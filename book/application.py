import os
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
	raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
	try:
		username = request.form.get("username")
		password = request.form.get("password")
		if(username == "" or password == ""):
			return "Please enter a valid username or password"

		if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
			db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
			db.commit()
			return render_template("login.html")
		else:
			return "Username has been taken"
	except:
		return render_template("login.html")

@app.route("/signup", methods=["POST"])
def signup():
	return render_template("signup.html")

@app.route("/mainpage", methods=["POST", "GET"])
def mainpage():
	try:
		username = request.form.get("username")
		password = request.form.get("password")

		books = db.execute("SELECT * FROM books").fetchall()

		if username == None:
			return render_template("main.html", books=books)
		if (db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 1) and (db.execute("SELECT * FROM users WHERE password = :password", {"password": password}).rowcount == 1):
			return render_template("main.html", books=books)
		else:
			return "wrong lol"
	except:
		return render_template("login.html")

@app.route("/books", methods=["GET"])
def books():
	"""LISTS all flights."""
	books = db.execute("SELECT * FROM books").fetchall()
	return render_template('books.html', books=books)

@app.route("/books/<int:book_id>", methods=["POST", "GET"])
def book(book_id):
	book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
	return book.title

@app.route("/books/result", methods=["POST"])
def result():
	book_name = request.form.get("book_name")
	return book_name


