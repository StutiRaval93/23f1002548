from flask import Flask, render_template, request, redirect
from models import db, Student , Company, Admin, Drive, Application

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


@app.route("/company_register", methods=["GET","POST"])
def company_register():

    if request.method == "POST":

        company_name = request.form["company_name"]
        email = request.form["email"]
        password = request.form["password"]

        new_company = Company(
            company_name=company_name,
            email=email,
            password=password
        )

        db.session.add(new_company)
        db.session.commit()

        return "Company Registered"

    return render_template("company_register.html")

@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # hard-coded admin
        if username == "admin" and password == "admin123":
            # List all unapproved companies
            companies = Company.query.filter_by(approved=False).all()
            drives = Drive.query.filter_by(status="Pending").all()

            return render_template("admin_dashboard.html", companies=companies, drives=drives)
        else:
            return "Invalid Credentials"
    return render_template("admin_login.html")

@app.route("/approve_company/<int:company_id>", methods=["POST"])
def approve_company(company_id):
    company = Company.query.get(company_id)
    company.approved = True
    db.session.commit()
    return "Company Approved Successfully"

@app.route('/company_login', methods=['GET','POST'])
def company_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        company = Company.query.filter_by(email=email, password=password).first()

        if company:

            if company.approved:
                return render_template("company_dashboard.html", company=company)

            else:
                return "Waiting for admin approval"

        else:
            return "Invalid credentials"

    return render_template("company_login.html")

@app.route('/create_drive', methods=['GET','POST'])
def create_drive():

    if request.method == 'POST':

        company_id = request.form['company_id']
        job_title = request.form['job_title']
        description = request.form['description']

        drive = Drive(
            company_id=company_id,
            job_title=job_title,
            description=description,
            status="Pending"
        )

        db.session.add(drive)
        db.session.commit()

        return "Placement Drive Created. Waiting for Admin Approval."

    return render_template("create_drive.html")

@app.route('/approve_drive/<int:id>', methods=['POST'])
def approve_drive(id):

    drive = Drive.query.get(id)

    drive.status = "Approved"

    db.session.commit()

    return redirect('/admin_login')

@app.route('/student_login', methods=['GET','POST'])
def student_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        student = Student.query.filter_by(email=email, password=password).first()

        if student:
            return redirect(f"/student_dashboard/{student.id}")

        else:
            return "Invalid credentials"

    return render_template("student_login.html")

@app.route('/student_dashboard/<int:student_id>')
def student_dashboard(student_id):

    student = Student.query.get(student_id)

    drives = Drive.query.filter_by(status="Approved").all()

    applications = Application.query.filter_by(student_id=student_id).all()

    return render_template(
        "student_dashboard.html",
        student=student,
        drives=drives,
        applications=applications
    )

@app.route('/apply/<int:student_id>/<int:drive_id>', methods=['POST'])
def apply(student_id, drive_id):

    existing = Application.query.filter_by(
        student_id=student_id,
        drive_id=drive_id
    ).first()

    if existing:
        return "Oops! You already applied for this drive"

    application = Application(
        student_id=student_id,
        drive_id=drive_id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()

    return "Wohoo! Application Submitted Successfully"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)