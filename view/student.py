import pymysql
from flask import Blueprint, render_template, Flask, request, redirect, session, json, current_app as app, jsonify
import hashlib, time
# from models import conn
from public import r
import datetime

student = Blueprint('student', __name__)


def get_a_conn():
    return pymysql.connect(host='152.136.124.24', user='root', password='123456', db='web',
                           cursorclass=pymysql.cursors.DictCursor, connect_timeout=120)


@student.route('/student/index')
def student_index():
    return render_template('/student/index.html')


@student.route('/student/class')
def student_class():
    return render_template('/student/class.html')


# 展示所有课程
@student.route('/student/show_all_section')
def show_all_sections():
    return render_template('/student/show_all_section.html')


@student.route('/student/get_all_sections')
def get_all_sections():
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('show_all_sections')
    res = cursor.fetchall()
    cursor.callproc('student_get_all_course_schedule')
    schedule = cursor.fetchall()
    cursor.close()
    conn.close()
    for item in schedule:
        # 提取timedelta类型的时间间隔
        time_delta1 = item['start_time']
        time_delta2 = item['end_time']
        # 计算总秒数
        total_seconds1 = int(time_delta1.total_seconds())
        total_seconds2 = int(time_delta2.total_seconds())
        # 将总秒数转换为datetime.time对象
        time_obj1 = datetime.time(total_seconds1 // 3600, (total_seconds1 % 3600) // 60, total_seconds1 % 60)
        time_obj2 = datetime.time(total_seconds2 // 3600, (total_seconds2 % 3600) // 60, total_seconds2 % 60)
        # 将datetime.time对象格式化为字符串
        time_str1 = time_obj1.strftime('%H:%M:%S')
        time_str2 = time_obj2.strftime('%H:%M:%S')
        # 将字符串类型的时间更新到字典的start_time属性上
        item['start_time'] = time_str1
        item['end_time'] = time_str2
    idx = 0
    idx_all = len(schedule)
    for row in res:
        sec_id = row['sec_id']
        children = []
        while idx < idx_all:
            the_sec_id = schedule[idx]['sec_id']
            if the_sec_id > sec_id:
                break
            elif the_sec_id == sec_id:
                children.append(schedule[idx])
            idx += 1
        row['children'] = children


    print(res[0])
    data = {'rows': res}
    return r(data)


# 展示已选课程
@student.route('/student/show_my_section')
def show_my_sections():
    return render_template('/student/show_my_section.html')


@student.route('/student/get_my_sections')
def get_my_sections():
    student_id = session['uid']
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('get_courses_for_student', (student_id,))
    res = cursor.fetchall()
    cursor.callproc('student_get_my_course_schedule', (student_id,))
    schedule = cursor.fetchall()
    cursor.close()
    conn.close()
    # 假设data为一个字典数组，每一项都包含一个名为start_time的timedelta属性

    for item in schedule:
        # 提取timedelta类型的时间间隔
        time_delta1 = item['start_time']
        time_delta2 = item['end_time']
        # 计算总秒数
        total_seconds1 = int(time_delta1.total_seconds())
        total_seconds2 = int(time_delta2.total_seconds())
        # 将总秒数转换为datetime.time对象
        time_obj1 = datetime.time(total_seconds1 // 3600, (total_seconds1 % 3600) // 60, total_seconds1 % 60)
        time_obj2 = datetime.time(total_seconds2 // 3600, (total_seconds2 % 3600) // 60, total_seconds2 % 60)
        # 将datetime.time对象格式化为字符串
        time_str1 = time_obj1.strftime('%H:%M:%S')
        time_str2 = time_obj2.strftime('%H:%M:%S')
        # 将字符串类型的时间更新到字典的start_time属性上
        item['start_time'] = time_str1
        item['end_time'] = time_str2
    idx = 0
    idx_all = len(schedule)
    for row in res:
        sec_id = row['sec_id']
        children = []
        while idx < idx_all:
            the_sec_id = schedule[idx]['sec_id']
            if the_sec_id > sec_id:
                break
            elif the_sec_id == sec_id:
                children.append(schedule[idx])
            idx += 1
        row['children'] = children
    data = {'rows': res}
    return r(data)


# 查分数
@student.route('/student/score')
def score():
    return render_template('/student/score.html')


@student.route('/student/get_my_score')
def get_my_score():
    student_id = session['uid']
    semester = request.values.get('semester', '')
    year = request.values.get('year', '')
    semester = '%' + semester + '%'
    year = '%' + year + '%'
    conn = get_a_conn()
    cursor = conn.cursor()
    # print((student_id, semester, year))
    cursor.callproc('student_get_score', (student_id, semester, year))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    # print(res)
    data = {'rows': res}
    return r(data)


# 获取班级信息
@student.route('/student/get_student_class_info')
def get_student_class_info():
    student_id = session['uid']
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('GET_CLASS_MEMBERS', (student_id,))
    res = cursor.fetchall()
    cursor.callproc('get_student_info', (student_id,))
    ans = cursor.fetchall()
    class_id = ans[0]['class_id']
    session['cid'] = class_id

    cursor.close()
    conn.close()
    # print(res)
    data = {'rows': res}
    return r(data)


# # 学生给老师打分
@student.route('/student/rate_teacher', methods=['GET', 'POST'])
def rate_teacher():
    return render_template('/student/rate_teacher.html')


@student.route('/student/rate_teacher_show_course')
def rate_teacher_show_course():
    student_id = session['uid']
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('student_get_evaluation_courses', (student_id,))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    data = {'rows': res}
    return r(data)


@student.route('/student/rating_teacher', methods=['POST'])
def rating_teacher():
    data = request.get_data()
    j_data = json.loads(data)
    student_id = session['uid']
    sec_id = j_data.get('sec_id', '')
    score = j_data.get('scores', '')
    comment = j_data.get('comment', '')
    parm = (student_id, sec_id, score, comment)
    conn = get_a_conn()
    cursor = conn.cursor()
    print(parm)
    sql1 = "select rate_teacher(%s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'Success: The teacher has been rated.':
        return r({}, 1, result)
    conn.commit()
    conn.close()
    return r({}, 0, '评分成功')


# 展示个人信息
@student.route('/student/my_info', methods=['GET', 'POST'])
def student_my_info():
    if request.method == 'GET':
        return render_template('student/my_info.html')
    data = request.get_data()
    j_data = json.loads(data)
    student_id = int(j_data.get('student_id', ''))
    account = j_data.get('account', '')
    name = j_data.get('name', '')
    password = j_data.get('password', '')
    sex = j_data.get('sex', '')
    tel = j_data.get('tel', '')
    id_card = j_data.get('id_card', '')
    detail = j_data.get('detail', '')
    parm = (student_id, name, password, sex, id_card, tel, detail)
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select update_student_info(%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    if result != 'info update successfully':
        return r({}, 1, result)
    conn.commit()
    conn.close()
    return r({}, 0, '成功修改信息')


@student.route('/student/get_me/<int:student_id>')
def student_get_me(student_id):
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select * from student where student_id = %s"
    cursor.execute(sql1, (student_id,))
    result = cursor.fetchone()
    # print(result)
    return r(result)


# 选课
@student.route('/student/section_selection')
def section_selection():
    return render_template('/student/section_selection.html')


@student.route('/student/show_section_selection')
def show_section_selection():
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('show_section_selection')
    res = cursor.fetchall()
    cursor.callproc('student_get_selection_schedule')
    schedule = cursor.fetchall()
    cursor.close()
    conn.close()
    for item in schedule:
        # 提取timedelta类型的时间间隔
        time_delta1 = item['start_time']
        time_delta2 = item['end_time']
        # 计算总秒数
        total_seconds1 = int(time_delta1.total_seconds())
        total_seconds2 = int(time_delta2.total_seconds())
        # 将总秒数转换为datetime.time对象
        time_obj1 = datetime.time(total_seconds1 // 3600, (total_seconds1 % 3600) // 60, total_seconds1 % 60)
        time_obj2 = datetime.time(total_seconds2 // 3600, (total_seconds2 % 3600) // 60, total_seconds2 % 60)
        # 将datetime.time对象格式化为字符串
        time_str1 = time_obj1.strftime('%H:%M:%S')
        time_str2 = time_obj2.strftime('%H:%M:%S')
        # 将字符串类型的时间更新到字典的start_time属性上
        item['start_time'] = time_str1
        item['end_time'] = time_str2
    idx = 0
    idx_all = len(schedule)
    for row in res:
        sec_id = row['sec_id']
        children = []
        while idx < idx_all:
            the_sec_id = schedule[idx]['sec_id']
            if the_sec_id > sec_id:
                break
            elif the_sec_id == sec_id:
                children.append(schedule[idx])
            idx += 1
        row['children'] = children
    data = {'rows': res}
    return r(data)


@student.route('/student/section_selection_operation', methods=['POST'])
def section_selection_operation():
    data = request.get_data()
    j_data = json.loads(data)
    student_id = session['uid']
    sec_id = j_data.get('sec_id', '')
    sec_id = int(sec_id)
    parm = (student_id, sec_id)
    conn = get_a_conn()
    cursor = conn.cursor()
    print(parm)
    sql1 = "select select_course(%s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    print(result)
    if result != 'Course selected successfully':
        return r({}, 1, result)
    conn.commit()
    conn.close()
    return r({}, 0, '选课成功！')


# 退课
@student.route('/student/section_withdrawal', methods=['GET', 'POST'])
def section_withdrawal():
    return render_template('/student/section_withdrawal.html')


@student.route('/student/show_section_withdrawal')
def show_section_withdrawal():
    student_id = session['uid']
    conn = get_a_conn()
    cursor = conn.cursor()
    cursor.callproc('show_section_withdrawal', (student_id,))
    res = cursor.fetchall()
    cursor.callproc('student_get_withdrawal_schedule', (student_id, ))
    schedule = cursor.fetchall()
    cursor.close()
    conn.close()
    for item in schedule:
        # 提取timedelta类型的时间间隔
        time_delta1 = item['start_time']
        time_delta2 = item['end_time']
        # 计算总秒数
        total_seconds1 = int(time_delta1.total_seconds())
        total_seconds2 = int(time_delta2.total_seconds())
        # 将总秒数转换为datetime.time对象
        time_obj1 = datetime.time(total_seconds1 // 3600, (total_seconds1 % 3600) // 60, total_seconds1 % 60)
        time_obj2 = datetime.time(total_seconds2 // 3600, (total_seconds2 % 3600) // 60, total_seconds2 % 60)
        # 将datetime.time对象格式化为字符串
        time_str1 = time_obj1.strftime('%H:%M:%S')
        time_str2 = time_obj2.strftime('%H:%M:%S')
        # 将字符串类型的时间更新到字典的start_time属性上
        item['start_time'] = time_str1
        item['end_time'] = time_str2
    idx = 0
    idx_all = len(schedule)
    for row in res:
        sec_id = row['sec_id']
        children = []
        while idx < idx_all:
            the_sec_id = schedule[idx]['sec_id']
            if the_sec_id > sec_id:
                break
            elif the_sec_id == sec_id:
                children.append(schedule[idx])
            idx += 1
        row['children'] = children
    data = {'rows': res}
    return r(data)


@student.route('/student/section_withdrawal_operation', methods=['POST'])
def section_withdrawal_operation():
    data = request.get_data()
    j_data = json.loads(data)
    student_id = session['uid']
    sec_id = j_data.get('sec_id', '')
    sec_id = int(sec_id)
    parm = (student_id, sec_id)
    conn = get_a_conn()
    cursor = conn.cursor()
    print(parm)
    sql1 = "select drop_course(%s, %s)"
    cursor.execute(sql1, parm)
    result = list(cursor.fetchone().values())[0]
    print(result)
    if result != 'Course dropped successfully':
        return r({}, 1, result)
    conn.commit()
    conn.close()
    return r({}, 0, '退课成功！')
