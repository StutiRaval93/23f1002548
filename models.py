from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    approved = db.Column(db.Boolean, default=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    course = db.Column(db.String(100))

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    job_role = db.Column(db.String(200))
    salary = db.Column(db.String(100))
    deadline = db.Column(db.String(100))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'))
    status = db.Column(db.String(100), default="Applied")

class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    job_title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    status = db.Column(db.String(50))