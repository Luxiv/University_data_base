
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students3.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost/students'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# stud_course = db.Table('stud_course',
#                        db.Column('student_id', db.Integer, db.ForeignKey('student.s_id')),
#                        db.Column('course_id', db.Integer, db.ForeignKey('course.c_id'))
#                        )


# Associatin Table:
class Stud_Course(db.Model):
    __tablename__ = 'stud_course'
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id',
                                                    ondelete='CASCADE'))
    course_id = db.Column(db.Integer(), db.ForeignKey('course.id',
                                                    ondelete='CASCADE'))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    students_in_group = db.relationship('Student', backref='group', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'ID: {self.id} Group {self.name}'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    courses = db.relationship("Course", secondary='stud_course',
                              backref=db.backref('student', lazy='dynamic'))

    def __init__(self, first_name, last_name, group_id):
        self.first_name = first_name
        self.last_name = last_name
        self.group_id = group_id

    def __repr__(self):
        return f'ID: {self.id} Student {self.first_name} {self.last_name} '


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(150), unique=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'ID: {self.id} Course {self.name}'


