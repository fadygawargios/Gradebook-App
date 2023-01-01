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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        # Store new teacher into database
        if int(db.execute("SELECT COUNT(google_id) FROM users WHERE google_id = ?;", session["google_id"])[0]["COUNT(google_id)"]) == 0:
            db.execute("INSERT INTO users VALUES (?, ?);", session["name"], session["google_id"])

        # Get teacher's info
        info = db.execute("SELECT * FROM users WHERE google_id = ?;", session["google_id"])
        return render_template("index.html", name=info[0]["name"])


@app.route("/classes", methods=["GET"])
@login_required
def classes():

    # Get classes from SQL db
    classes = db.execute("SELECT class_code, class_name, class_colour FROM classes WHERE teacher_id = ?", session["google_id"])


    
    return render_template("classes.html", classes=classes)


@app.route("/class", methods=["GET", "POST"])
@login_required
def class_page():
    if request.method == "POST":
        code = request.args.get("code")

        unit = request.form.get("unit")

        if unit == "new":
            unit = request.form.get("new_unit")
    
        name = request.form.get("task_name")
        weight = request.form.get("weight")
        description = request.form.get("description")
        # Hidden input
        code = request.form.get("code")

        class_id = db.execute("SELECT rowID FROM classes WHERE teacher_id = ? AND class_code = ?", session["google_id"], code)[0]["rowid"]

        db.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?);", name, description, class_id, unit, weight)
       
        flash("Ajouter!")
        return redirect(f"/class?code={code}")

    else:
        # Get tasks
        code = request.args.get("code")
        class_info = db.execute("SELECT rowID, * FROM classes WHERE teacher_id = ? AND class_code = ?;", session["google_id"], code)[0]
    
        # Get a list of all the units
        units = db.execute("SELECT DISTINCT unit FROM tasks WHERE class_id = ?;", class_info["rowid"])

        unit_list = []
        
        for unit in units:
            unit_list.append(unit["unit"])


        tasks_dict = {}

        task_length = {}
        
        # Cycle through the list of units getting all tasks that match said unit from SQL
        
        for unit in unit_list:
            tasks = db.execute("SELECT name, description, weight FROM tasks WHERE class_id = ? AND unit = ?;", class_info["rowid"], unit)
            
            # Count the number of tasks in each unit
            total = len(tasks)
            task_length[unit] = total

            # Append those task to the part with the units...
            tasks_dict[unit] = tasks


        return render_template("class.html", class_info=class_info, tasks=tasks_dict, units=unit_list, length=task_length)


@app.route("/task", methods=["GET", "POST"])
@login_required
def task():
    if request.method == "POST":
        return "not yet"
    else:
        name = request.args.get("task")
        # Get class code
        class_code = db.execute("SELECT class_code FROM classes WHERE rowID = (SELECT class_id FROM tasks WHERE name = ?);", name)[0]["class_code"]
        
        # Get students
        students = []
        student_names = db.execute("SELECT student_name FROM students WHERE class_code = ?;", class_code)
        for student in student_names:
            students.append(student["student_name"])
        
        #task_name = request.args.get("name")
        return render_template("task.html", class_code=class_code, students=students)

@app.route("/students", methods=["GET", "POST"])
@login_required
def students():
    if request.method == "POST":
        return ("not implemented yet")
    else:
        # Get students from SQL db
        classes = db.execute("SELECT class_code, class_name FROM classes WHERE teacher_id = ?", session["google_id"])


        # Dictionary for students and class
        student_class = {}
        # https://thispointer.com/python-dictionary-with-multiple-values-per-key/

        
        for x in range(len(classes)):
            class_name = classes[x]["class_name"]
            
            # Add student_emails after...
            students = db.execute("SELECT student_name FROM students WHERE class_code = (SELECT class_code FROM classes WHERE teacher_id = ? AND class_name = ?);", session["google_id"], class_name)
           
            students_in_class = []
            for student in students:
               students_in_class.append(student["student_name"])

            student_class[class_name] = students_in_class
            
        return render_template("students.html", classes=classes, student_class=student_class)



@app.route("/welcome", methods=["GET"])
def welcome():
    return render_template("welcome.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST": 

        class_code = request.form.get("class_code")
        class_name = request.form.get("class_name")
        class_colour = request.form.get("class_colour")

        # TB: re-arranged
        db.execute("INSERT INTO classes (class_name, class_colour, teacher_id, class_code) VALUES (?, ?, ?, ?);", class_name, class_colour, session["google_id"], class_code)

        # Add the students to class-student table
        student_name = []

        # TB added as a feature
        student_email = []
        i = 1

        while request.form.get("name_" + str(i)) != None:
        
            student_name.append(request.form.get("name_" + str(i)))    
            i += 1
        
        for student in student_name:
            db.execute("INSERT INTO students (class_code, student_name) VALUES (?, ?);", class_code, student)


            # Alert the user that it has been created
        flash("Créer!")
        return redirect("/classes")
    
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
    app.run(debug=True)
