"""Instaeater."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request
# flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension

# from model import connect_to_db, db, Post


app = Flask(__name__)

# app.secret_key = "ABC"

# app.jinja_env.undefined = StrictUndefined

@app.route('/')
def login():
	"""Users must log in before accessing the site."""

	return render_template("login.html")


if __name__ == "__main__":
    app.debug = True
    # connect_to_db(app)
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0")



