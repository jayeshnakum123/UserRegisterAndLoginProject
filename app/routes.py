from flask import request, redirect, render_template, flash, session

from app import app, db

from app.models import Auth, user_signin

from flask import after_this_request

from datetime import timedelta


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        number = request.form["number"]

        new_user = user_signin(username=username, email=email, mobile=number)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! You can now log in.")
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # user = user_signin.query.filter_by(username=username, password=password).first()
        user = user_signin.query.filter_by(username=username).first()

        if user:
            if user.check_password(password):
                session["username"] = user.username
                session["email"] = user.email
                session["mobile"] = user.mobile

                flash(f"Logged in successfully! Welcome '{username}'")
                return render_template("index.html", username=username)
            else:
                error_message = "Invalid Password !!"
        else:
            error_message = "Invalid UserName !!"
        flash(error_message)
    return render_template("login.html")


@app.route("/profile", methods=["GET"])
def profile():
    if request.method == "GET":
        if session:
            print(session["username"])
            return render_template("profile.html", profile_data=session)
    return redirect("/")


# @app.route("/logout")
# def logout():
#     session.pop("username", None)
#     session.pop("email", None)
#     session.pop("mobile", None)
#     session.clear()
#     return redirect("/")


def add_header(response):
    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    )
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        session.pop("username", None)
        session.pop("email", None)
        session.pop("mobile", None)
        session.clear()

        @after_this_request
        def add_no_cache_header(response):
            return add_header(response)

    else:
        if request.method == "GET":
            return redirect("/")
    return redirect("/")
