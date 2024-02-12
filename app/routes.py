from flask import request, redirect, render_template, flash

from app import app, db

from app.models import Auth, user_signin


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        number = request.form["number"]

        new_user = user_signin(
            username=username, password=password, email=email, mobile=number
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! You can now log in.")
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    # return "Hello Login form..."
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = user_signin.query.filter_by(username=username, password=password).first()

        if user:
            print(f"User found {user.username},{user.password}")
            flash("Logged in successfully!")
            return render_template("index.html")
        else:
            flash("Invalid Username or Password! Please try again.")
    return render_template("login.html")
