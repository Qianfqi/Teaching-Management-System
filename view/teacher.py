from flask import Blueprint, render_template, Flask, request, redirect, session, json, current_app as app
import hashlib, time
from tools import get_a_conn
from public import r
import datetime
from tools import *
from urllib.parse import unquote
teacher = Blueprint('teacher', __name__)


@teacher.route('/teacher')
@teacher.route('/teacher/index')
def teacher_index():
    return render_template('/teacher/index.html')


@teacher.route('/teacher/manage_info')
def teacher_manage_info():
    return render_template("/teacher/manage_info.html")


@teacher.route('/teacher/get_teacher_info')
def teacher_get_teacher_info():
    data = {}
    conn = get_a_conn()
    cursor = conn.cursor()
    uid = session['uid']
    cursor.callproc('get_teacher_info', (uid,))
    print(uid)
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    data['rows'] = items
    print(data)
    return r(data)


@teacher.route('/teacher/update_teacher_info', methods=['POST'])
def teacher_update_teacher_info():
    data = request.get_data()
    j_data = json.loads(data)
    teacher_id = int(j_data.get('teacher_id', ''))
    account = j_data.get('account', '')
    name = j_data.get('name', '')
    password = j_data.get('password', '')
    sex = j_data.get('sex', '')
    tel = j_data.get('tel', '')
    sign = j_data.get('sign', '')
    parm = (teacher_id,account, name, password, sex, tel, sign)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "call update_teacher_info(%s,%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '修改成功:')


@teacher.route('/teacher/class')
def teacher_class():
    return render_template('/teacher/class.html')


@teacher.route('/teacher/get_all_students')
def teacher_get_student():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    c_id = int(request.values.get('c_id', -1))
    s_id = int(request.values.get('s_id', -1))
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    uid = session['uid']
    print(c_id)
    if s_id != -1:
        cursor.callproc('get_class_students',(uid,None,s_id))
    elif c_id != -1:
        cursor.callproc('get_class_students', (uid,c_id,None))
    else:
        cursor.callproc('get_class_students', (uid, None,None))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows)}
    return r(data)


@teacher.route('/teacher/update_student_info',methods=['POST'])
def  teacher_update_student_info():
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
    class_id = (j_data.get('class_id', ''))
    id_card = j_data.get('id_card', '')
    grade = (j_data.get('grade'))
    parm = (student_id, account, name, password, sex, tel, detail, class_id, id_card, in_time, grade)
    print(parm)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select admin_change_a_student(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    print(parm)
    cursor.execute(sql1, parm)
    print(parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'success':
        cursor.close()
        conn.close()
        return r({}, 1, '修改失败')
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '成功修改:')


@teacher.route('/teacher/course')
def teacher_course():
    return render_template('/teacher/course.html')


@teacher.route('/teacher/get_course')
def teacher_get_course():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    offset = (page - 1) * perPage
    sec_id = int(request.values.get('sec_id',-1))
    conn = get_a_conn()
    cursor = conn.cursor()
    uid = session['uid']
    if sec_id == -1:
        cursor.callproc('get_teacher_courses', (uid,None))
    else:
        cursor.callproc('get_teacher_courses', (uid,sec_id))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows)}
    return r(data)


@teacher.route('/teacher/course_table')
def teacher_course_table():
    return render_template("/teacher/course_table.html")


@teacher.route('/teacher/get_course_table')
def teacher_get_course_table():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    sec_id = int(request.values.get('sec_id',-1))
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    uid = session['uid']
    if sec_id == -1:
        cursor.callproc('get_teacher_courses_info', (uid,None))
    else:
        cursor.callproc('get_teacher_courses_info', (uid,sec_id))
    rows = cursor.fetchall()
    for i in range(len(rows)):
        rows[i]['start_time'] = str(rows[i]['start_time'])
        rows[i]['end_time'] = str(rows[i]['end_time'])
        print(rows[i])
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows)}
    return r(data)


@teacher.route('/teacher/student')
def teacher_student():
    return render_template('/teacher/student.html')


@teacher.route('/teacher/get_select_student')
def teacher_get_select_student():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    s_id = int(request.values.get('s_id', 0))
    offset = (page - 1) * perPage
    conn = get_a_conn()
    cursor = conn.cursor()
    uid = session['uid']
    if s_id == 0:
        cursor.callproc('get_select_students', (uid, None))
    else:
        cursor.callproc('get_select_students', (uid,s_id))
    rows = cursor.fetchall()
    for i in range(len(rows)):
        if rows[i]['tag'] == 0:
            rows[i]['tag'] = "未上传"
        else:
            rows[i]['tag'] = "已上传"

    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows)}
    return r(data)


@teacher.route('/teacher/update_student_score',methods=['POST'])
def teacher_update_student_score():
    print("success")
    data = request.get_data()
    j_data = json.loads(data)
    sec_id = int(j_data.get('sec_id', ''))
    student_id = j_data.get('student_id', '')
    score= int(j_data.get('score', ''))
    teacher_id =int( session['uid'])
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "call update_student_score(%s,%s, %s,%s)"
    parm = (teacher_id,sec_id,student_id,score)
    cursor.execute(sql1, parm)
    conn.commit()
    cursor.close()
    conn.close()
    return r({}, 0, '修改成功:')


@teacher.route('/teacher/score')
def teacher_get_score():
    return render_template('/teacher/score.html')


@teacher.route('/teacher/get_student_score')
def teacher_get_student_score():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    offset = (page - 1) * perPage
    s_id = int(request.values.get('s_id', -1))
    u_id = session['uid']
    conn = get_a_conn()
    cursor = conn.cursor()
    print(s_id)
    if s_id != -1:
        cursor.callproc("sp_get_student_courses", (s_id,u_id))
        rows = cursor.fetchall()
    else:
        rows = []
    for row in rows:
        row['s_id'] = s_id
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows)}
    return r(data)


@teacher.route('/teacher/evaluation')
def teacher_evaluation():
    return render_template('/teacher/evaluation.html')

@teacher.route('/teacher/get_evaluation')
def teacher_get_evaluation():
    perPage = int(request.values.get('perPage'))
    page = int(request.values.get('page'))
    offset = (page - 1) * perPage
    s_id = int(request.values.get('s_id', -1))
    u_id = session['uid']
    conn = get_a_conn()
    cursor = conn.cursor()
    print(s_id)
    if s_id != -1:
        cursor.callproc("teacher_get_evaluation", (u_id, s_id))
    else:
        cursor.callproc("teacher_get_evaluation",(u_id,None))
    rows = cursor.fetchall()
    for row in rows:
        row['s_id'] = s_id
    cursor.close()
    conn.close()
    data = {'rows': rows[offset:offset + perPage], 'total': len(rows)}
    return r(data)





