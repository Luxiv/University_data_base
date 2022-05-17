from app import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

stud_course = db.Table('stud_course',
                       db.Column('student_id', db.Integer, db.ForeignKey('student.s_id')),
                       db.Column('course_id', db.Integer, db.ForeignKey('course.c_id'))
                       )


class Group(db.Model):
    g_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    students_in_group = db.relationship('Student', backref='group', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'ID: {self.id} Group {self.name}'


class Student(db.Model):
    s_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=True)
    last_name = db.Column(db.String(50), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.g_id'))
    courses = db.relationship("Course", secondary=stud_course,
                              backref=db.backref('student', lazy='dynamic'))

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'ID: {self.s_id} Student {self.first_name} {self.last_name} '


class Course(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(50), unique=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'ID: {self.c_id} Course {self.name}'
