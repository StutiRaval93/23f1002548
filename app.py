from flask import Flask, render_template, request
from models import db, Student

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student_register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        course = request.form["course"]

        new_student = Student(
            name=name,
            email=email,
            password=password,
            course=course
        )

        db.session.add(new_student)
        db.session.commit()

        return "Student Registered Successfully"

    return render_template("student_register.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)