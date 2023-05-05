from flask import Flask, render_template,request,redirect,url_for
import mysql.connector
app=Flask(__name__)

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="picknflix"
)

cursor=db.cursor()


@app.route("/")
def Home_Page():
    return render_template("home.html")

@app.route("/signup.html")
def signup():
    return render_template("signup.html")

@app.route("/login.html")
def login():
    return render_template("login.html")    

@app.route("/info.html")
def aboutus():
    return render_template("info.html")

@app.route("/recommendations.html")
def recommendations():
    cursor.execute("select distinct Genre from recommendations")
    listGenres=cursor.fetchall()
    return render_template("recommendations.html", lists=listGenres)


@app.route("/Recommendations/Random")
def randomfilm():
    selectrandom="select * from recommendations order by RAND() limit 1"
    cursor.execute(selectrandom)
    randomlist=cursor.fetchall()
    return render_template("genre.html", film=randomlist)


@app.route("/Recommendations/<genre>")
def randomgenre(genre):
    selectQuery="select * from recommendations where Genre= '"+genre+"' order by RAND() limit 1"
    cursor.execute(selectQuery)
    filmlist=cursor.fetchall()
    return render_template("genre.html", film=filmlist, gname=genre)

@app.route("/newfilm")
def newRecord():
    return render_template("newfilm.html")

@app.route("/saverecord",methods=["POST"])
def saverecord():
    cursor.execute("insert into recommendations values('"+ request.form['genrename']+"','"+request.form['filmname']+"')")
    db.commit()
    return redirect(url_for('Home_Page'))

@app.route("/Filmshowings")
def listfilms():
    findshowings="select * from film"
    cursor.execute(findshowings)
    showings=cursor.fetchall()
    return render_template("showtimes.html", show=showings)

@app.route("/Filmshowings/<fname>")
def findshowings(fname):
    findshowings="select event.Date, event.Time from filmevent join event on filmevent.Eventid = event.id WHERE filmevent.filmid = (SELECT film.id FROM film WHERE film.Film = %s)"
    cursor.execute(findshowings, (fname,))
    showings=cursor.fetchall()
    return render_template("showtimes.html", time=showings )

def findcinema(cname):
    findcinema="SELECT cinema.CinemaName FROM filmcinema JOIN cinema ON filmcinema.Cinemaid=cinema.id WHERE filmcinema.filmid = (SELECT film.id FROM film WHERE film.Film = %s)"
    cursor.execute(findcinema, (cname,))
    location=cursor.fetchall()
    return render_template("showtimes.html", cinema=location )




app.run(debug=True)   