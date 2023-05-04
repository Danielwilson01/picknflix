from flask import Flask, render_template,request,redirect,url_for
import mysql.connector
app=Flask(__name__)

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="films"
)

cursor=db.cursor()


@app.route("/")
def Home_Page():
    cursor.execute("select distinct Cinema from johnwick")
    listshowings=cursor.fetchall()
    return render_template("listings.html", lists=listshowings)


# @app.route("/")
# def Home_Page():
#     cursor.execute("select table_name from information_schema.tables WHERE table_schema = 'films'")
#     listshowings=cursor.fetchall()
#     return render_template("listings.html", lists=listshowings)


# @app.route("/filmshowings/<cname>")
# def findshowings(cname):
#     findshowings="select * from 'johnwick' where table_name='"+cname+"'"
#     cursor.execute(findshowings)
#     showings=cursor.fetchall()
#     return render_template("showtimes.html", show=showings, Cinema=cname)

@app.route("/filmshowings/<cname>")
def findshowings(cname):
    findshowings="select * from johnwick where Cinema='"+cname+"'"
    cursor.execute(findshowings)
    showings=cursor.fetchall()
    return render_template("showtimes.html", show=showings, Cinema=cname)

# **select table_schema Schema_Name ,table_name TableName,column_name ColumnName,ordinal_position "Position",column_type DataType,COUNT(1) ColumnCount
# FROM information_schema.columns
# GROUP by table_schema,table_name,column_name,ordinal_position, column_type;**

app.run(debug=True)   