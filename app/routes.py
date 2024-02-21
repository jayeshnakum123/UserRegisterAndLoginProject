from flask import (
    request,
    redirect,
    render_template,
    flash,
    session,
)

from app import app, db

from app.models import Auth, user_signin, User_queries

from flask import after_this_request

from datetime import timedelta

from flask_wtf.file import FileField, FileAllowed

from werkzeug.utils import secure_filename

from flask_mail import Mail

import os

import json

file_path = "config.json"


# app.config["UPLOAD_FOLDER"] = "uploads"
app.config["UPLOAD_FOLDER"] = "app/static/uploads"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

# mail send karva mate no code che
with open("config.json", "r") as c:
    params = json.load(c)["params"]
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT="465",
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params["gmail-user"],
    MAIL_PASSWORD=params["gmail-password"],
)
mail = Mail(app)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        number = request.form["number"]
        profile_picture = request.files["profile_picture"]

        if profile_picture and allowed_file(profile_picture.filename):
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            filename = "default.jpg"

        new_user = user_signin(
            username=username,
            email=email,
            mobile=number,
            profile_picture=filename,
        )
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
        user = user_signin.query.filter_by(username=username).first()

        if user:
            if user.check_password(password):
                session["username"] = user.username
                session["email"] = user.email
                session["mobile"] = user.mobile
                session["id"] = user.id
                session["profile_picture"] = user.profile_picture

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
            # print(session["username"])
            return render_template("profile.html", profile_data=session)
    return redirect("/")


def add_header(response):
    response.headers.add(
        "Cache-Control",
        "no-store, no-cache, must-revalidate, post-check=0, pre-check=0",
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


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    # user = user_signin.query.get(id)
    user = user_signin.query.filter_by(id=id).first()
    return render_template("updateData.html", user=user)


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    user = user_signin.query.get(id)

    if request.method == "POST" and user:
        username = request.form.get("username")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        profile_picture = request.files.get("profile_picture")

        if profile_picture and allowed_file(profile_picture.filename):
            filename = secure_filename(profile_picture.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            profile_picture.save(filepath)
            user.update_profile(username, email, mobile, filename)
            return render_template("profile.html", profile_data=user)
        else:
            # Handle invalid file format
            flash(
                "Invalid file format. Allowed formats are png, jpg, jpeg, gif.", "error"
            )

        user.update_profile(username, email, mobile, profile_picture)
        return render_template("profile.html", profile_data=user)
    return render_template("login.html", profile_data=user)


# Contact-Us Page Routes Code.


@app.route("/contactUs", methods=["GET", "POST"])
def contactUs():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        number = request.form["number"]
        message = request.form["message"]

        user_queries = User_queries(
            name=name, email=email, number=number, message=message
        )
        db.session.add(user_queries)
        db.session.commit()

        # je pan email id malse te email id thi aapna mail account ma mail aavse te no code.
        mail.send_message(
            "New Message From " + name,
            sender=email,
            recipients=[
                # "pritish.sus@gmail.com"
                # "bhautikchothani.sus@gmail.com"
                params["gmail-user"]
            ],  # jene mail mokal vo hoi tenu email id
            body=f"Name: {name}\n Email: {email}\n Phone: {number}\n Message: {message}",
        )
    return redirect("/")
