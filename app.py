from flask import render_template, request
from models import Group, Student, Course, StudCourse as stud_course, db, app
from api import api


@app.route('/groups/', methods=['GET'])
def Groups():
    """
    Groups/Group info
    :return: text/html
    """
    grp_info = Group.query.all()
    group_ids_list = [std.group_id for std in Student.query.all()]
    numbr_stds_in_grp = {grp.id: group_ids_list.count(grp.id) for grp in Group.query.all()}

    if request.args.get('group_id'):
        group = request.args.get('group_id')
        std_info = Student.query.filter(Student.group_id == int(group))
        return render_template('group.html', group_id=int(group),
                               stds=std_info, grps=grp_info, numbr_stds_in_grp=numbr_stds_in_grp)

    elif request.args.get('count'):
        """ to implement function 'Find all groups with less or equals student count' """
        grps_less_equal_count = [grp_id for grp_id, numbr in numbr_stds_in_grp.items()
                                 if numbr <= int(request.args.get('count'))]
        return render_template('groups_less_eq.html', grps_l_e=grps_less_equal_count, grps=grp_info,
                               numbr_stds_in_grp=numbr_stds_in_grp)

    return render_template('groups.html', grps=grp_info, numbr_stds_in_grp=numbr_stds_in_grp)


@app.route('/students/', methods=('POST', 'GET'))
def Students():
    """
    Students/Student info
    :return: text/html
    """
    std_info = Student.query.all()
    if request.args.get('student_id'):
        grp_info = Group.query.all()
        crs_info = Course.query.all()
        tbl = stud_course.query.all()
        student = request.args.get('student_id')
        if request.form.get('rem_std'):
            '''Remove student'''
            try:
                s = Student.query.filter_by(id=int(student)).first()
                db.session.delete(s)
                db.session.commit()
                return render_template('student_removed.html', title='Student')
            except:
                db.session.rollback()
                print('Removing error')

        elif request.form.get('rem_crs'):
            '''Remove student from course'''
            try:
                c = stud_course.query.filter_by(student_id=int(student),
                                                course_id=request.form.get('courses')).first()
                db.session.delete(c)
                db.session.commit()
                return render_template('student_removed.html', title='Course')
            except:
                db.session.rollback()
                print('Removing error')

        return render_template('student.html', info=std_info, grps=grp_info,
                               crss=crs_info, id=int(student), tbl=tbl)
    return render_template('students.html', info=std_info)


@app.route('/courses/', methods=['POST', 'GET', 'PUT'])
def Courses():
    """
    Courses/Course info
    :return: text/html
    """
    crs_info = Course.query.all()
    if request.args.get('course_id'):
        tbl = stud_course.query.all()
        std_info = Student.query.all()
        grp_info = Group.query.all()
        course = request.args.get('course_id')
        if request.form.get('add_std'):
            """ Add student on course from list"""
            try:
                stds_course_id = [std.course_id for std in stud_course.query.filter_by(
                    student_id=request.form.get('students'))]
                if int(course) not in stds_course_id:
                    c = stud_course(student_id=request.form.get('students'), course_id=course)
                    db.session.add(c)
                    db.session.commit()
            except:
                db.session.rollback()
                print('Assign  error')

        return render_template('course.html', stds=std_info, grps=grp_info,
                               crss=crs_info, id=int(course), tbls=tbl)
    return render_template('courses.html', crss=crs_info)


@app.route('/add_student', methods=('POST', 'GET'))
def registration():
    """
    Registration for students
    :return: text/html
    """
    if request.method == 'POST':
        try:
            s = Student(first_name=request.form['first name'],
                        last_name=request.form['last name'],
                        group_id=request.form['group id'])
            db.session.add(s)
            db.session.flush()

            c = stud_course(student_id=s.id, course_id=request.form['course'])
            db.session.add(c)
            db.session.commit()
        except:
            db.session.rellback()
            print('Registration error')

    return render_template('student_reg.html', title='Registration')


if __name__ == '__main__':
    app.run()
