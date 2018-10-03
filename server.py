"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request, flash, session

from model import User, Ratings_data, Movie, connect_to_db, db

from model import connect_to_db, db


db = SQLAlchemy()
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    userlist = User.query.all()
    return render_template("user_list.html", users=userlist)

@app.route('/sign_up')
def show_form():
    """Show registration form"""

    return render_template("sign_up_form.html")

@app.route('/submit', methods = ["POST"])
def sign_up():
    """Submit form information"""

    user_email = request.form.get("email")
    pass_word = request.form.get("password")

    user = User(email = user_email, password =pass_word)
    db.session.add(user)
    db.session.commit()
    userlist = User.query.all()
    return render_template("user_list.html", users=userlist)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
