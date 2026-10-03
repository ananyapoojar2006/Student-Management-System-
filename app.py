from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "student_management_secret_key"

DATA_FILE = "students.json"

USERS_FILE = "users.json"

# Load students from JSON file
def load_students():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return []


# Save students to JSON file
def save_students(students):
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)
# Load users
def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except:
        return []


# Save users
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


# Home page
@app.route("/")
def home():

    # Check login
    if "username" not in session:
        return redirect(url_for("login"))

    students = load_students()

    search = request.args.get("search", "").strip().lower()

    if search:
        students = [
            student for student in students
            if search in student["name"].lower()
            or search in student["roll"].lower()
            or search in student["course"].lower()
        ]

    return render_template(
        "index.html",
        students=students,
        search=search
    )
# Add student
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        students = load_students()

        student = {
    "id": len(students) + 1,
    "name": request.form["name"],
    "roll": request.form["roll"],
    "course": request.form["course"],
    "email": request.form["email"],
    "phone": request.form["phone"],
    "gender": request.form["gender"],
    "department": request.form["department"],
    "semester": request.form["semester"],
    "dob": request.form["dob"],
    "address": request.form["address"]
}

        students.append(student)
        save_students(students)

        return redirect(url_for("home"))

    return render_template("add_student.html")


# Delete student
@app.route("/delete/<int:id>")
def delete_student(id):

    students = load_students()

    students = [
        student for student in students
        if student["id"] != id
    ]

    save_students(students)

    return redirect(url_for("home"))


# Edit student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    students = load_students()

    student = next(
        (student for student in students if student["id"] == id),
        None
    )

    if student is None:
        return redirect(url_for("home"))

    if request.method == "POST":

        student["name"] = request.form["name"]
        student["roll"] = request.form["roll"]
        student["course"] = request.form["course"]
        student["email"] = request.form["email"]
        student["phone"] = request.form["phone"]

        save_students(students)

        return redirect(url_for("home"))

    return render_template(
        "edit_student.html",
        student=student
    )
# Registration
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        users = load_users()

        username = request.form["username"]
        password = request.form["password"]

        # Check if username already exists
        for user in users:
            if user["username"] == username:
                return render_template(
                    "register.html",
                    error="Username already exists"
                )

        user = {
            "username": username,
            "password": password
        }

        users.append(user)

        save_users(users)

        return redirect(url_for("login"))

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        users = load_users()

        username = request.form["username"]
        password = request.form["password"]

        for user in users:

            if (
                user["username"] == username
                and user["password"] == password
            ):

                session["username"] = username

                return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("login"))


# Run application
if __name__ == "__main__":
    app.run(debug=True)