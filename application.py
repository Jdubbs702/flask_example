from flask import Flask, redirect, url_for, render_template, request, session, flash
from admin.admin import admin
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.register_blueprint(admin, url_prefix="/admin")
application.secret_key = "hello"
# application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
# application.config["SQLALCHEMY_DATABASE_URI"] = "mysql://username:password@localhost/db_name"
# application.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Chief1%40Le%40!@localhost/users"
application.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:Chief10Leo!@aws-database1.cqexgqnfzh0u.us-east-1.rds.amazonaws.com/picture_this"
application.config["SQLAlchemy_TRACK_MODIFICATIONS"] = False
application.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(application)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@application.route("/")
def home():
    return render_template("index.html")


@application.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))

        return render_template("login.html")


@application.route("/user", methods=["POST", "GET"])
def user():
    email = None
    print(f"email: {email}")
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]

        print(f"email: {email}")
        return render_template("user.html", user=user, email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


@application.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@application.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    with application.app_context():
        db.create_all()
    application.run(debug=True)

# delete syntax: found_user = users.query.filter_by(name=user).delete()
# multiple items in query to delete? :
#   for user in found_user:
#       user.delete()
