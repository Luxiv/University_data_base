from flask import Flask, render_template, request
from models import Group, Student, Course, app, Stud_Course as stud_course






@app.route('/groups/')
def Groups():  # put application's code here
    grp_info = Group.query.all()
    if request.args.get('group'):
        group = request.args.get('group')
        std_info = Student.query.filter(Student.group_id == int(group))
        return render_template('group.html', group_id=int(group), stds=std_info, grps=grp_info)
    return render_template('groups.html', grps=grp_info)


@app.route('/students/', methods=['GET'])
def Students():
    std_info = Student.query.all()
    if request.args.get('student_id'):
        grp_info = Group.query.all()
        crs_info = Course.query.all()
        tbl = stud_course.query.all()
        student = request.args.get('student_id')
        return render_template('student.html', info=std_info, grps=grp_info, crss=crs_info, id=int(student), tbl=tbl)
    return render_template('students.html', info=std_info)


@app.route('/courses/', methods=['GET'])
def Courses():
    crs_info = Course.query.all()
    if request.args.get('course_id'):
        tbl = stud_course.query.all()
        std_info = Student.query.all()
        grp_info = Group.query.all()
        course = request.args.get('course_id')
        return render_template('course.html', stds=std_info, grps=grp_info, crss=crs_info, id=int(course), tbls=tbl)
    return render_template('courses.html', crss=crs_info)


if __name__ == '__main__':
    app.run()
