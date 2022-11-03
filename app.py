import os
import pathlib
import requests
from re import L

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_session import Session
from functools import wraps
from pip._vendor import cachecontrol

# Google Oauth
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests

GOOGLE_CLIENT_ID = "829293429363-02ps2499vf9n30qu62b57rb75movtp2v.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
    )

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")



def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        try:
            name = session["name"]
        except (KeyError, ValueError):
            return redirect("/welcome")
        return function(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Alert message
message = ""

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
        name = session["name"]
        return render_template("index.html", name=name)


@app.route("/classes", methods=["GET"])
@login_required
def classes():
    # Get classes from SQL db
    return render_template("classes.html")



@app.route("/students", methods=["GET", "POST"])
@login_required
def students():
    if request.method == "POST":
        return ("not implement yet")
    else:
        # Get students from SQL db
        return render_template("students.html")



@app.route("/welcome", methods=["GET"])
def welcome():
    return render_template("welcome.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        return "working on it"
    else:
        return render_template("create.html")


@app.route("/login", methods=["GET"])
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)


    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/welcome")


if __name__ == "__main__":
    app.run()
