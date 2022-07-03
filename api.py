from flask_restx import Api, Resource, fields
from flask import request
from models import Group, Student, Course, StudCourse, db
from app_config import app

VERSION = '1.0'
api = Api(app, doc='/apidocs/', version=VERSION, title='FoxmindEd university API',
          description='API helps you to get all information of university')
ns = api.namespace(f'api/{VERSION}', description='API INFO')


group_parser = ns.parser()
group_parser.add_argument('group_id', location='args')
course_parser = ns.parser()
course_parser.add_argument('course_id', location='args')
student_parser = ns.parser()
student_parser.add_argument('student_id', location='args')

student_course_model = ns.model('student_course_model', {
    'student_id': fields.Integer
})
student_model = ns.model('student_model', {
    'course_id': fields.Integer})
add_student_model = ns.model('add_student_model', {
    'First name': fields.String,
    'Last name': fields.String,
    'Group id': fields.Integer,
    'Course id': fields.Integer
})


@ns.route('/groups/')
@ns.expect(group_parser)
@ns.doc(params={'group_id': '1-10'})
class Groups(Resource):
    def get(self):
        """
                    Info about groups
        To get students in group, pleas pass group id
        """
        group_ids_list = [std.group_id for std in Student.query.all()]
        group_info = {f'ID: {grp.id}': [f'Name: {grp.name}', f'Students in group: {group_ids_list.count(grp.id)}']
                      for grp in Group.query.all()}
        args = group_parser.parse_args()
        if args.group_id:
            group_info = {std.id: [std.first_name, std.last_name]
                          for std in Student.query.all()
                          if std.group_id == int(args.group_id)}
        return group_info


@ns.route('/courses/')
class Courses(Resource):
    @ns.expect(course_parser)
    @ns.doc(params={'course_id': '1-10'})
    def get(self):
        """
                Info about courses
        To get students on course, pleas pass course id

        """
        courses_info = {crs.id: crs.name for crs in Course.query.all()}
        args = course_parser.parse_args()

        if args.course_id:
            courses_info = {std.id: [std.first_name, std.last_name]
                            for row in StudCourse.query.filter_by(course_id=int(args.course_id))
                            for std in Student.query.filter_by(id=row.student_id).all()}
        return courses_info

    @ns.expect(student_course_model, course_parser)
    def post(self):
        """
        To assign student to the course
            pleas pass student id
        """
        args = course_parser.parse_args()
        if args.course_id:
            sc = StudCourse(course_id=int(args.course_id), student_id=request.json['student_id'])
            db.session.add(sc)
            db.session.commit()
            return {'message': 'data updated'}


@ns.route('/students/')
class Students(Resource):
    @ns.expect(student_parser)
    def get(self):
        """
                 Get info about students
         To get info about student pleas pass student id
        """
        args = student_parser.parse_args()
        students_info = {std.id: [std.first_name, std.last_name, f'group id: {std.group_id}',
                         f'courses id: {[crs.course_id for crs in StudCourse.query.filter_by(student_id=std.id)]}']
                         for std in Student.query.all()}

        if args.student_id:
            students_info = {std.id: [std.first_name, std.last_name, f'group id: {std.group_id}',
                             f'courses id: {[crs.course_id for crs in StudCourse.query.filter_by(student_id=std.id)]}']
                             for std in Student.query.filter_by(id=int(args.student_id))}
        return students_info

    @ns.expect(student_parser, student_model)
    def put(self):
        """
        Remove student from course
        """
        args = student_parser.parse_args()

        association_id = [row.id for row in
                          StudCourse.query.filter_by(course_id=request.json['course_id'],
                                                     student_id=int(args.student_id))]

        c = StudCourse.query.get(association_id)
        db.session.delete(c)
        db.session.commit()
        return {'message': 'Course deleted successfully'}

    @ns.expect(student_parser)
    def delete(self):
        """
            Delete student
        pleas pass student id
        """
        args = student_parser.parse_args()
        s = Student.query.get(int(args.student_id))
        db.session.delete(s)
        db.session.commit()
        return {'message': 'Student deleted successfully'}


@ns.route('/add_student')
class AddStudent(Resource):
    @ns.expect(add_student_model)
    def post(self):
        """
         Student Registration
        Pleas pass the fields
        """
        s = Student(first_name=request.json['First name'],
                    last_name=request.json['Last name'],
                    group_id=request.json['Group id'])
        db.session.add(s)
        db.session.flush()

        c = StudCourse(student_id=s.id, course_id=request.json['Course id'])
        db.session.add(c)
        db.session.commit()
        return {'message': 'data updated'}
