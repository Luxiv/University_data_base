from models import db, Student, Course, Group
from models import Stud_Course as stud_course
from info_generators import Student_Gen, Course_Gen, Group_Gen
import random

def groups_upload(group_number):
    try:
        for group_name in Group_Gen().group_gene8or(group_number):
            g = Group(name=group_name)
            db.session.add(g)
            print(f'Group {group_name}')
        db.session.commit()
        print(f'{group_number} groups are uploaded to db')
    except:
        db.session.rollback()
        print('Db group adding error')



def group_id_gen(used_id, id_list):
    '''
    Its function helper for func stud_upload() that randomly assign students to groups.
    Each group could contain from 10 to 30 students.
    It is possible that some students will be without groups
    :param used_id:
    :param id_list:
    :return: group_id
    '''
    for group_id in id_list:
        used_id.append(group_id)
        if used_id.count(group_id) <= random.choice(range(10, 31)):
            return group_id


def stud_upload(stud_number):
    '''
    :return:
    '''
    try:
        used_id = []
        group_ids_list = [i.id for i in Group.query.all()]
        for ful_name in Student_Gen().student_gene8or(stud_number):
            fn = ful_name.split()
            s = Student(first_name=fn[0], last_name=fn[1], group_id=group_id_gen(used_id, group_ids_list))
            db.session.add(s)
        db.session.commit()
        print(f'{stud_number} students are uploaded to db')
    except:
        db.session.rollback()
        print('Db student adding error')



def course_upload():
    try:
        for course in Course_Gen().courses_list():
            c = Course(name=course, description=f'On this course you going to study {course}!')
            db.session.add(c)
        db.session.commit()
        print('All courses are uploaded to db')
    except:
        db.session.rollback()
        print('Db courses adding error')



# def students_courses_assignation():
#     try:
#         for std in Student.query.all():
#             number_courses_for_one_student = random.choice(range(1, 4))
#             used_courses_list = []
#             for j in range(1, number_courses_for_one_student + 1):
#                 course = random.choice(Course.query.all())
#                 if course not in used_courses_list:
#                     statement = stud_course.insert().values(student_id=std.s_id, course_id=course.c_id)
#                     db.session.execute(statement)
#
#                     print(f'Student: {std.s_id} course: {course.name}')
#                 used_courses_list.append(course)
#             print('______________________________')
#         db.session.commit()
#     except:
#         db.session.rollback()
#         print('Db assignation error')

def students_courses_assignation():
    try:
        for std in Student.query.all():
            number_courses_for_one_student = random.choice(range(1, 4))
            used_courses_list = []
            for j in range(1, number_courses_for_one_student + 1):
                course = random.choice(Course.query.all())
                if course not in used_courses_list:
                    statement = stud_course(student_id=std.id, course_id=course.id)
                    db.session.add(statement)

                    print(f'Student: {std.id} course: {course.name}')
                used_courses_list.append(course)
            print('______________________________')
        db.session.commit()
    except:
        db.session.rollback()
        print('Db assignation error')


groups_upload(10)
stud_upload(200)
course_upload()
students_courses_assignation()
