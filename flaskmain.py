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

i=0

@app.route("/")
def Home_Page():
    return render_template("home.html")

@app.route("/Index")
def Index():
    return render_template("index.html")


@app.route("/Signup")
def signup():
    return render_template("signup.html")

@app.route("/Login")
def login():
    return render_template("login.html")    

@app.route("/Aboutus")
def aboutus():
    return render_template("info.html")

@app.route("/Recommendations")
def recommendations():
    return render_template("recommendations.html")

@app.route("/Partners")
def Partners():
    return render_template("partners.html")

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

@app.route("/Filmshowings/")
def listfilms():
    headings=("Film", "Runtime", "Age Rating")
    findshowings="select film.id, film, runtime, agerating.rating from film join agerating where agerating.id=film.agerating;"
    cursor.execute(findshowings)
    showings=cursor.fetchall()
    return render_template("showtimes.html", headings=headings, show=showings)

@app.route("/Filmshowings/<fname>")
def findshowings(fname):
    findshowings="select event.id, film.film, event.date, event.time from event join filmevent on event.id=filmevent.eventid join film on filmevent.filmid=film.id where filmevent.filmid=%s"
    cursor.execute(findshowings, (fname,))
    time=cursor.fetchall()
    return render_template("showtimes.html", time=time, fname=fname)

@app.route("/Filmshowings/<fname>/<event>")
def findvenue(fname, event):
    findvenue = "SELECT cinema.id, film, cinemaname, event.date, event.time FROM cinema JOIN film JOIN event ON film.id = film.id WHERE film.id = %s AND event.id = %s"
    heading=("Film", "Venue", "Date", "Time")
    cursor.execute(findvenue, (fname, event))
    venue = cursor.fetchall()
    return render_template("showtimes.html", location=venue, fname=fname, event=event, heading=heading)


app.run(debug=True)   