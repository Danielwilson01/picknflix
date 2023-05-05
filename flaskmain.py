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


@app.route("/Random")
def randomfilm():
    selectrandom="select * from recommendations order by RAND() limit 1"
    cursor.execute(selectrandom)
    randomlist=cursor.fetchall()
    return render_template("random.html", film=randomlist)


@app.route("/Comedy")
def randomcomedy():
    selectQuery="select * from recommendations where Genre='Comedy' order by RAND() limit 1"
    cursor.execute(selectQuery)
    comedylist=cursor.fetchall()
    return render_template("comedy.html", film=comedylist)

@app.route("/Action")
def randomaction():
    selectQuery="select * from recommendations where Genre='Action' order by RAND() limit 1"
    cursor.execute(selectQuery)
    actionlist=cursor.fetchall()
    return render_template("action.html", film=actionlist)

@app.route("/Romance")
def randomromance():
    selectQuery="select * from recommendations where Genre='Romance' order by RAND() limit 1"
    cursor.execute(selectQuery)
    romlist=cursor.fetchall()
    return render_template("romance.html", film=romlist)
    
@app.route("/Horror")
def randomhorror():
    selectQuery="select * from recommendations where Genre='Horror' order by RAND() limit 1"
    cursor.execute(selectQuery)
    horrorlist=cursor.fetchall()
    return render_template("horror.html", film=horrorlist)

@app.route("/Heroes")
def randomheroes():
    selectQuery="select * from recommendations where Genre='Heroes' order by RAND() limit 1"
    cursor.execute(selectQuery)
    herolist=cursor.fetchall()
    return render_template("heroes.html", film=herolist)

@app.route("/newfilm")
def newRecord():
    return render_template("newfilm.html")

@app.route("/saverecord",methods=["POST"])
def saverecord():
    cursor.execute("insert into recommendations values('"+ request.form['genrename']+"','"+request.form['filmname']+"')")
    db.commit()
    return redirect(url_for('Home_Page'))

@app.route("/filmshowings")
def listfilms():
    findshowings="select * from film"
    cursor.execute(findshowings)
    showings=cursor.fetchall()
    return render_template("showtimes.html", show=showings)

@app.route("/filmshowings/<fname>")
def findshowings(fname):
    findshowings="select event.Date, event.Time from filmevent join event on filmevent.Eventid = event.id WHERE filmevent.filmid = (SELECT film.id FROM film WHERE film.Film = %s)"
    cursor.execute(findshowings, (fname,))
    showings=cursor.fetchall()
    return render_template("showtimes.html", time=showings )


app.run(debug=True)   