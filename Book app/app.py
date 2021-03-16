import os
from flask import Flask,session,request,render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
app=Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)
engine=create_engine("postgres://tlnwvirnaevntm:e36f788edfe26911e9472643beb07f6064845f4c06c7e94e48e5a29f4108c0b1@ec2-34-202-7-83.compute-1.amazonaws.com:5432/d8hqspblimdhtr")
db=scoped_session(sessionmaker(bind=engine))
@app.route("/")
def index():
    return(render_template("index.html"))
@app.route("/signup")
def signup():
    return(render_template("signup.html"))
@app.route("/logout")
def logout():
    return(render_template("logout.html"))
@app.route("/register",methods=["POST"])
def register():
    username=request.form.get("username")
    try:
        username = request.form.get("username")
    except ValueError:
        return render_template("error.html",message="invalid input")
    password=request.form.get("password")
    if (db.execute("SELECT * FROM users WHERE username=:username",{"username":username}).rowcount==0):
        db.execute("INSERT INTO users(username,password) VALUES (:username,:password)",
        {"username":username,"password":password})
        db.commit()
    else:
        return(render_template("error.html",message="username already exists"))
    return(render_template("success.html"))
@app.route("/login",methods=["POST"])
def login():
    username=request.form.get("username")
    password=request.form.get("password")
    user=db.execute("SELECT * FROM users WHERE username=:username AND password=:password",{"username":username,"password":password}).fetchall()
    if user:
        usr=db.execute("SELECT * FROM users WHERE username=:username and password=:password",{"username":username,"password":password}).fetchall()
        for id,username,password in usr:
            id=id
        print(id)
        return(render_template("search.html",id1=id))
    else:
        return(render_template("error.html",message="no user found"))
@app.route("/search/<int:user_id>",methods=["POST"])
def search(user_id):
    isbn=request.form.get("isbn")
    author=request.form.get("author")
    title="%"+request.form.get("title")+"%"
    title=title.title()
    #id=id1
    #print(id)

    #if author:
        #input=db.execute("SELECT * FROM books WHERE author LIKE '%' +author+ '%' ").fetchall()
    if title:
        input=db.execute("SELECT id,isbn,title,year,author FROM books WHERE title LIKE :title",{"title":title})
    return(render_template("view.html",input=input,user_id=user_id))
@app.route("/search/<int:user_id>/<int:book_id>",methods=["POST","GET"])
def book(user_id,book_id):
    rating=request.form.get("rating")
    comment=request.form.get("comment")
    alert=False
    if rating:
        if db.execute("SELECT * FROM review WHERE user_id=:user_id",{"user_id":user_id}).rowcount==0:
            db.execute("INSERT INTO review(rating,comment,book_id,user_id) VALUES(:rating,:comment,:book_id,:user_id)",{"rating":rating,"comment":comment,"book_id":book_id,"user_id":user_id})
            #db.execute("UPDATE reviews SET user_id=:user_id WHERE rating=:rating AND comment=:comment AND book_id:book_id",{"rating":rating,"comment":comment,"book_id":book_id})
            db.commit()
        else:
            alert=True

    riev=db.execute("SELECT rating,comment FROM review WHERE book_id=:book_id",{"book_id":book_id}).fetchall()
    buk=db.execute("SELECT * FROM books WHERE id=:id",{"id":book_id}).fetchone()

    return(render_template("book.html",book=buk,reviews=riev,id=user_id,alert=alert))
