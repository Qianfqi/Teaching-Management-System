import math
import random

from flask import Blueprint, render_template, Flask, request, redirect, session, json, current_app as app
import hashlib, time
from tools import get_a_conn
from public import r
import datetime
from tools import *


list_start_time = ['08:00:00', '10:00:00', '13:30:00', '15:30:00', '18:30:00']
list_end_time = ['09:40:00', '11:40:00', '15:10:00', '17:10:00', '20:10:00']
list_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

admin = Blueprint('admin', __name__)

@admin.route('/admin/test')
def admin_test():
    return render_template('/admin/test.html')


@admin.route('/admin')
@admin.route('/admin/index')
def admin_index():
    return render_template('/admin/index.html')


@admin.route('/admin/class')
def admin_class():
    return render_template('/admin/class.html')


@admin.route('/admin/teacher')
def admin_teacher():
    return render_template('/admin/teacher.html')


@admin.route('/admin/student')
def admin_student():
    return render_template('/admin/student.html')


@admin.route('/admin/department')
def admin_department():
    return render_template('/admin/department.html')


@admin.route('/admin/building')
def admin_building():
    return render_template('/admin/building.html')


@admin.route('/admin/classroom')
def admin_classroom():
    return render_template('/admin/classroom.html')


@admin.route('/admin/course', methods=['GET', 'POST'])
def admin_course():
    return render_template('/admin/course.html')


@admin.route('/admin/sec_course')
def admin_sec_course():
    return render_template('/admin/sec_course.html')


# -------------------teacher--------------------
@admin.route('/admin/add_a_teacher', methods=['POST'])
def admin_add_a_teacher():
    data = request.get_data()
    j_data = json.loads(data)
    in_time = str(datetime.date.fromtimestamp(int(j_data['in_time'])))
    teacher_id = int(j_data.get('teacher_id', ''))
    account = j_data.get('account', '')
    name = j_data.get('name', '')
    password = j_data.get('password', '')
    sex = j_data.get('sex', '')
    tel = j_data.get('tel', '')
    sign = j_data.get('sign', '')
    department_id = int(j_data.get('department_id', ''))
    id_card = j_data.get('id_card', '')
    parm = (teacher_id, account, name, password, sex, tel, sign, department_id, id_card, in_time)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_add_a_teacher(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功添加一个教师')


@admin.route('/admin/ini_teacher')
def admin_ini_teacher():
    data = {'department_options': get_department_options()}
    return r(data)


@admin.route('/admin/get_all_teacher')
def admin_get_all_teacher():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    name = request.values.get('name', '')
    id_card = request.values.get('id_card', '')
    name = '%' + name + '%'
    id_card = '%' + id_card + '%'
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('admin_get_all_teacher', (name, id_card))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows), 'department_options': get_department_options()}
    return r(data)


@admin.route('/admin/change_a_teacher', methods=['POST'])
def admin_change_a_teacher():
    data = request.get_data()
    j_data = json.loads(data)
    in_time = str(datetime.date.fromtimestamp(int(j_data['in_time'])))
    teacher_id = int(j_data.get('teacher_id', ''))
    account = j_data.get('account', '')
    name = j_data.get('name', '')
    password = j_data.get('password', '')
    sex = j_data.get('sex', '')
    tel = j_data.get('tel', '')
    sign = j_data.get('sign', '')
    department_id = j_data.get('department_id', '')
    id_card = j_data.get('id_card', '')
    parm = (teacher_id, account, name, password, sex, tel, sign, department_id, id_card, in_time)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_change_a_teacher(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功修改一个教师:' + str(teacher_id))


@admin.route('/admin/delete_a_teacher/<int:teacher_id>', methods=['DELETE'])
def admin_delete_a_teacher(teacher_id):
    sql1 = 'select admin_delete_a_teacher(%s)'
    conn = get_a_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql1, (teacher_id,))
        status = 0
        msg = '删除成功'
    except Exception as e:
        status = 1
        msg = str(e)
    if status == 0:
        conn.commit()
    cursor.close()
    conn.close()
    return r({}, status, msg)


@admin.route('/admin/repwd_a_teacher/<int:teacher_id>', methods=['PUT'])
def admin_repwd_a_teacher(teacher_id):
    sql1 = 'select admin_repwd_a_teacher(%s)'
    conn = get_a_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql1, (teacher_id,))
        status = 0
        msg = '重置成功:' + str(teacher_id)
    except Exception as e:
        status = 1
        msg = str(e)
    if status == 0:
        conn.commit()
    cursor.close()
    conn.close()
    return r({}, status, msg)


# -------------------student----------------------
@admin.route('/admin/get_all_student')
def admin_get_all_studnet():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    name = request.values.get('name', '')
    id_card = request.values.get('id_card', '')
    name = '%' + name + '%'
    id_card = '%' + id_card + '%'
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('admin_get_all_student', (name, id_card))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows), 'class_options': get_class_options()}
    return r(data)


@admin.route('/admin/repwd_a_student/<int:student_id>', methods=['PUT'])
def admin_repwd_a_student(student_id):
    sql1 = 'select admin_repwd_a_student(%s)'
    conn = get_a_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql1, (student_id,))
        status = 0
        msg = '重置成功:' + str(student_id)
    except Exception as e:
        status = 1
        msg = str(e)
    if status == 0:
        conn.commit()
    cursor.close()
    conn.close()
    return r({}, status, msg)


@admin.route('/admin/delete_a_student/<int:student_id>', methods=['DELETE'])
def admin_delete_a_student(student_id):
    sql1 = 'select admin_delete_a_student(%s)'
    conn = get_a_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql1, (student_id,))
        status = 0
        msg = '删除成功'
    except Exception as e:
        status = 1
        msg = str(e)
    if status == 0:
        conn.commit()
    cursor.close()
    conn.close()
    return r({}, status, msg)


@admin.route('/admin/ini_student')
def admin_ini_student():
    data = {'class_options': get_class_options()}
    return r(data)


@admin.route('/admin/add_a_student', methods=['POST'])
def admin_add_a_student():
    data = request.get_data()
    j_data = json.loads(data)
    in_time = str(datetime.date.fromtimestamp(int(j_data['in_time']))) if j_data['in_time'] != '' else ''
    student_id = int(j_data.get('student_id', ''))
    account = j_data.get('account', '')
    name = j_data.get('name', '')
    password = j_data.get('password', '')
    sex = j_data.get('sex', '')
    tel = j_data.get('tel', '')
    detail = j_data.get('detail', '')
    class_id = int(j_data.get('class_id', ''))
    grade = int(j_data.get('grade', ''))
    id_card = j_data.get('id_card', '')
    parm = (student_id, account, name, password, sex, tel, detail, class_id, grade, id_card, in_time)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_add_a_student(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功添加一个学生')


@admin.route('/admin/change_a_student', methods=['POST'])
def admin_change_a_student():
    data = request.get_data()
    j_data = json.loads(data)
    in_time = str(datetime.date.fromtimestamp(int(j_data['in_time']))) if j_data['in_time'] != '' else ''
    student_id = int(j_data.get('student_id', ''))
    account = j_data.get('account', '')
    name = j_data.get('name', '')
    password = j_data.get('password', '')
    sex = j_data.get('sex', '')
    tel = j_data.get('tel', '')
    detail = j_data.get('detail', '')
    class_id = int(j_data.get('class_id', ''))
    id_card = j_data.get('id_card', '')
    grade = int(j_data.get('grade'))
    parm = (student_id, account, name, password, sex, tel, detail, class_id, id_card, in_time, grade)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_change_a_student(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功修改一个学生:' + str(student_id))


# -------------class------------
@admin.route('/admin/ini_class')
def admin_ini_class():
    data = {'teacher_options': get_teacher_options()}
    return r(data)


@admin.route('/admin/get_all_class')
def admin_get_all_class():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    name = request.values.get('name', '')
    name = '%' + name + '%'
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('admin_get_all_class', (name,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows), 'teacher_options': get_teacher_options()}
    return r(data)


@admin.route('/admin/delete_a_class/<int:class_id>', methods=['DELETE'])
def admin_delete_a_class(class_id):
    sql1 = 'select admin_delete_a_class(%s)'
    conn = get_a_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql1, (class_id,))
        status = 0
        msg = '删除成功'
    except Exception as e:
        status = 1
        msg = str(e)
    if status == 0:
        conn.commit()
    cursor.close()
    conn.close()
    return r({}, status, msg)


@admin.route('/admin/add_a_class', methods=['POST'])
def admin_add_a_class():
    data = request.get_data()
    j_data = json.loads(data)
    class_id = int(j_data.get('class_id', ''))
    name = j_data.get('name', '')
    teacher_id = int(j_data.get('teacher_id', ''))
    parm = (class_id, name, teacher_id)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_add_a_class(%s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功添加一个班级')


@admin.route('/admin/change_a_class', methods=['POST'])
def admin_change_a_class():
    data = request.get_data()
    j_data = json.loads(data)
    class_id = int(j_data.get('class_id', ''))
    name = j_data.get('name', '')
    teacher_id = int(j_data.get('teacher_id', ''))
    parm = (class_id, name, teacher_id)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_change_a_class(%s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功修改一个教师:' + str(teacher_id))


# -------------department---------------
@admin.route('/admin/ini_department')
def admin_ini_department():
    return r({})


@admin.route('/admin/get_all_department')
def admin_get_all_department():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    name = request.values.get('name', '')
    name = '%' + name + '%'
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('admin_get_all_department', (name,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows)}
    return r(data)


@admin.route('/admin/delete_a_department/<int:department_id>', methods=['DELETE'])
def admin_delete_a_department(department_id):
    sql1 = 'select admin_delete_a_department(%s)'
    conn = get_a_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql1, (department_id,))
        status = 0
        msg = '删除成功'
    except Exception as e:
        status = 1
        msg = str(e)
    if status == 0:
        conn.commit()
    cursor.close()
    conn.close()
    return r({}, status, msg)


@admin.route('/admin/add_a_department', methods=['POST'])
def admin_add_a_department():
    data = request.get_data()
    j_data = json.loads(data)
    department_id = int(j_data.get('department_id', ''))
    name = j_data.get('name', '')
    parm = (department_id, name)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_add_a_department(%s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功添加一个学院')


@admin.route('/admin/change_a_department', methods=['POST'])
def admin_change_a_department():
    data = request.get_data()
    j_data = json.loads(data)
    department_id = int(j_data.get('department_id', ''))
    name = j_data.get('name', '')
    parm = (department_id, name)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_change_a_department(%s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功修改一个学院:' + str(department_id))


# -------------building------------
@admin.route('/admin/ini_building')
def admin_ini_building():
    data = {'department_options': get_department_options()}
    return r(data)


@admin.route('/admin/get_all_building')
def admin_get_all_building():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    name = request.values.get('name', '')
    name = '%' + name + '%'
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('admin_get_all_building', (name,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows), 'department_options': get_department_options()}
    return r(data)


@admin.route('/admin/delete_a_building/<int:building_id>', methods=['DELETE'])
def admin_delete_a_building(building_id):
    sql1 = 'select admin_delete_a_building(%s)'
    conn = get_a_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql1, (building_id,))
        status = 0
        msg = '删除成功'
    except Exception as e:
        status = 1
        msg = str(e)
    if status == 0:
        conn.commit()
    cursor.close()
    conn.close()
    return r({}, status, msg)


@admin.route('/admin/add_a_building', methods=['POST'])
def admin_add_a_building():
    data = request.get_data()
    j_data = json.loads(data)
    building_id = int(j_data.get('building_id', ''))
    name = j_data.get('name', '')
    department_id = int(j_data.get('department_id', ''))
    parm = (building_id, name, department_id)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_add_a_building(%s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功添加一个教学楼')


@admin.route('/admin/change_a_building', methods=['POST'])
def admin_change_a_building():
    data = request.get_data()
    j_data = json.loads(data)
    building_id = int(j_data.get('building_id', ''))
    name = j_data.get('name', '')
    department_id = int(j_data.get('department_id', ''))
    parm = (building_id, name, department_id)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_change_a_building(%s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功修改一个教学楼:' + str(department_id))


# -------------classroom------------
@admin.route('/admin/ini_classroom')
def admin_ini_classroom():
    data = {'building_options': get_building_options()}
    return r(data)


@admin.route('/admin/get_all_classroom')
def admin_get_all_classroom():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    name = request.values.get('name', '')
    name = '%' + name + '%'
    building_id = request.values.get('building_id', '')
    building_id = int(building_id) if building_id != '' else -1
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('admin_get_all_classroom', (name, building_id))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows), 'building_options': get_building_options()}
    return r(data)


@admin.route('/admin/delete_a_classroom/<int:classroom_id>', methods=['DELETE'])
def admin_delete_a_classroom(classroom_id):
    sql1 = 'select admin_delete_a_classroom(%s)'
    conn = get_a_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql1, (classroom_id,))
        status = 0
        msg = '删除成功'
    except Exception as e:
        status = 1
        msg = str(e)
    if status == 0:
        conn.commit()
    cursor.close()
    conn.close()
    return r({}, status, msg)


@admin.route('/admin/add_a_classroom', methods=['POST'])
def admin_add_a_classroom():
    data = request.get_data()
    j_data = json.loads(data)
    classroom_id = int(j_data.get('classroom_id', ''))
    name = j_data.get('name', '')
    building_id = int(j_data.get('building_id', ''))
    parm = (classroom_id, name, building_id)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_add_a_classroom(%s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功添加一个教室')


@admin.route('/admin/change_a_classroom', methods=['POST'])
def admin_change_a_classroom():
    data = request.get_data()
    j_data = json.loads(data)
    classroom_id = int(j_data.get('classroom_id', ''))
    name = j_data.get('name', '')
    building_id = int(j_data.get('building_id', ''))
    parm = (classroom_id, name, building_id)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_change_a_classroom(%s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功修改一教室:' + str(classroom_id))


# -------------course------------
@admin.route('/admin/ini_course')
def admin_ini_course():
    data = {'department_options': get_department_options()}
    return r(data)


@admin.route('/admin/get_all_course')
def admin_get_all_course():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    name = request.values.get('name', '')
    name = '%' + name + '%'
    department_id = request.values.get('department_id', '')
    department_id = int(department_id) if department_id != '' else -1
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('admin_get_all_course', (name, department_id))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows), 'department_options': get_department_options()}
    return r(data)


@admin.route('/admin/delete_a_course/<int:course_id>', methods=['DELETE'])
def admin_delete_a_course(course_id):
    sql1 = 'select admin_delete_a_course(%s)'
    conn = get_a_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql1, (course_id,))
        status = 0
        msg = '删除成功'
    except Exception as e:
        status = 1
        msg = str(e)
    if status == 0:
        conn.commit()
    cursor.close()
    conn.close()
    return r({}, status, msg)


@admin.route('/admin/add_a_course', methods=['POST'])
def admin_add_a_course():
    data = request.get_data()
    j_data = json.loads(data)
    course_id = int(j_data.get('course_id', ''))
    name = j_data.get('name', '')
    total_time = int(j_data.get('total_time', ''))
    grade = int(j_data.get('grade', ''))
    department_id = int(j_data.get('department_id', ''))
    parm = (course_id, name, total_time, grade, department_id)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_add_a_course(%s, %s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功添加一个课程')


@admin.route('/admin/change_a_course', methods=['POST'])
def admin_change_a_course():
    data = request.get_data()
    j_data = json.loads(data)
    course_id = int(j_data.get('course_id', ''))
    name = j_data.get('name', '')
    total_time = int(j_data.get('total_time', ''))
    grade = int(j_data.get('grade', ''))
    department_id = int(j_data.get('department_id', ''))
    parm = (course_id, name, total_time, grade, department_id)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_change_a_course(%s, %s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功修改一个课程:' + str(course_id))


# -------------sec_course------------
@admin.route('/admin/ini_sec_course')
def admin_ini_sec_course():
    data = {'classroom_options': get_class_options(),
            'course_options': get_course_options()}
    return r(data)


@admin.route('/admin/get_all_sec_course')
def admin_get_all_sec_course():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    classroom_id = request.values.get('classroom_id', '')
    classroom_id = int(classroom_id) if classroom_id != '' else -1
    course_id = request.values.get('course_id', '')
    course_id = int(course_id) if course_id != '' else -1
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('admin_get_all_sec_course', (classroom_id, course_id))
    rows = cursor.fetchall()
    cursor.callproc('admin_get_all_course_schedule')
    course_schedule = cursor.fetchall()
    cursor.close()
    conn.close()
    total = len(rows)
    rows = rows[offset:offset + perPage]
    idx = 0
    idx_all = len(course_schedule)
    for row in rows:
        sec_id = row['sec_id']
        children = []
        while idx < idx_all:
            the_sec_id = course_schedule[idx]['sec_id']
            if the_sec_id > sec_id:
                break
            elif the_sec_id == sec_id:
                children.append(course_schedule[idx])
            idx += 1
        row['children'] = children
    data = {'rows': rows, 'total': total, 'classroom_options': get_classroom_options(),
            'course_options': get_course_options()}
    return r(data)


@admin.route('/admin/delete_a_sec_course/<int:sec_id>', methods=['DELETE'])
def admin_delete_a_sec_course(sec_id):
    sql1 = 'select admin_delete_a_sec_course(%s)'
    conn = get_a_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql1, (sec_id,))
        status = 0
        msg = '删除成功'
    except Exception as e:
        status = 1
        msg = str(e)
    if status == 0:
        conn.commit()
    cursor.close()
    conn.close()
    return r({}, status, msg)


@admin.route('/admin/add_a_sec_course', methods=['POST'])
def admin_add_a_sec_course():
    data = request.get_data()
    j_data = json.loads(data)
    sec_id = int(j_data.get('sec_id', ''))
    semester = j_data.get('semester', '')
    total_capacity = int(j_data.get('total_capacity', ''))
    current_capacity = 0
    classroom_id = int(j_data.get('classroom_id', ''))
    course_id = int(j_data.get('course_id', ''))
    year = int(j_data.get('year', ''))
    conn = get_a_conn()
    cursor = conn.cursor()
    sql2 = "select total_time from course where course_id=%s"
    cursor.execute(sql2, (course_id,))
    total_time = cursor.fetchone()['total_time']
    course_schedule = admin_cal_course_schedule(sec_id, total_time, year, semester)
    print(course_schedule)
    if len(course_schedule) == 0:
        cursor.close()
        conn.close()
        return r({}, 1, '没有空闲的教室了')
    parm = (sec_id, semester, total_capacity, current_capacity, classroom_id, course_id, year)
    sql1 = "select admin_add_a_sec_course(%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    for row in course_schedule:
        sql3 = "insert course_schedule(sec_id, day_of_week, start_time, end_time, start_week, end_week) values(%s, " \
               "%s, %s, %s, %s, %s) "
        end_week = 18 if row != course_schedule[-1] else math.ceil((total_time - (len(course_schedule) - 1) * 18 * 1.5) / 1.5)
        cursor.execute(sql3, (sec_id, random.choice(list_week), row[1], row[2], 1, end_week))
    print('yes')
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功添加一个开课')


@admin.route('/admin/change_a_sec_course', methods=['POST'])
def admin_change_a_sec_course():
    data = request.get_data()
    j_data = json.loads(data)
    sec_id = int(j_data.get('sec_id', ''))
    semester = j_data.get('semester', '')
    total_capacity = int(j_data.get('total_capacity', ''))
    current_capacity = int(j_data.get('current_capacity', ''))
    if total_capacity < current_capacity:
        return r({}, 1, '总容量小于已选课程人数')
    classroom_id = int(j_data.get('classroom_id', ''))
    course_id = int(j_data.get('course_id', ''))
    year = int(j_data.get('year', ''))
    parm = (sec_id, semester, total_capacity, current_capacity, classroom_id, course_id, year)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_change_a_sec_course(%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, result)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功修改一个开课:' + str(sec_id))


# -----------change_me-------------
@admin.route('/admin/change_me', methods=['GET', 'POST'])
def admin_change_me():
    if request.method == 'GET':
        return render_template('admin/change_me.html')
    data = request.get_data()
    j_data = json.loads(data)
    admin_id = int(j_data.get('admin_id', ''))
    account = j_data.get('account', '')
    name = j_data.get('name', '')
    password = j_data.get('password', '')
    sex = j_data.get('sex', '')
    tel = j_data.get('tel', '')
    id_card = j_data.get('id_card', '')
    parm = (admin_id, account, name, password, sex, tel, id_card)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_change_me(%s, %s, %s, %s, %s, %s, %s)"
    # cursor.execute(sql1, parm)
    try:
        cursor.execute(sql1, parm)
        result = list(cursor.fetchone().values())[0]
        if result != 'success':
            cursor.close()
            conn.close()
            return r({}, 1, result)
    except Exception as e:
        return r({}, 1, str(e))
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '修改成功')


@admin.route('/admin/get_me/<int:admin_id>')
def admin_get_me(admin_id):
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select * from admin where admin_id = %s"
    cursor.execute(sql1, (admin_id,))
    result = cursor.fetchone()
    return r(result)


def admin_cal_course_schedule(sec_id, total_time, year, semester):
    parma = (year, semester)
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('admin_get_empty_classroom', parma)
    result1 = cursor.fetchall()
    cursor.callproc('admin_get_clear_classroom', parma)
    result2 = cursor.fetchall()
    times = math.ceil(total_time / 1.5)
    n_times = math.ceil(times / 18)
    result = []
    if n_times > 5 * len(result2):
        return []
    id = 0
    cnt = 0
    while cnt < n_times:
        result.append([result2[id]['classroom_id'], list_start_time[cnt % 5], list_end_time[cnt % 5]])
        cnt += 1
        if cnt % 5 == 0:
            id += 1
    return result
