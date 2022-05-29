import unittest
from api import db
from app import app
import flask

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1@localhost/students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
TESTING = True


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = app
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_students_valid_route(self):
        tester = app.test_client()
        response = tester.get('/students/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_groups_valid_route(self):
        tester = app.test_client()
        response = tester.get('/groups/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_courses_valid_route(self):
        tester = app.test_client()
        response = tester.get('/courses/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_requests_student_id(self):
        with app.test_request_context('/students/?student_id=1'):
            assert flask.request.path == '/students/'
            assert flask.request.args['student_id'] == '1'

    def test_requests_group_id(self):
        with app.test_request_context('/groups/?group_id=2'):
            assert flask.request.path == '/groups/'
            assert flask.request.args['group_id'] == '2'

    def test_requests_course_id(self):
        with app.test_request_context('/courses/?course_id=10'):
            assert flask.request.path == '/courses/'
            assert flask.request.args['course_id'] == '10'

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = app
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
