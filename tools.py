import pymysql


def get_a_conn():
    return pymysql.connect(host='152.136.124.24', user='root', password='123456', db='web',
                           cursorclass=pymysql.cursors.DictCursor, connect_timeout=120)


def get_department_options():
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select * from department"
    cursor.execute(sql1)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    arr = []
    for one in result:
        arr.append({'label': one['name'], 'value': one['department_id']})
    return arr


def get_class_options():
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select * from class"
    cursor.execute(sql1)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    arr = []
    for one in result:
        arr.append({'label': one['name'], 'value': one['class_id']})
    return arr


def get_teacher_options():
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select * from teacher"
    cursor.execute(sql1)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    arr = []
    for one in result:
        arr.append({'label': one['name'], 'value': one['teacher_id']})
    return arr


def get_building_options():
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select * from building"
    cursor.execute(sql1)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    arr = []
    for one in result:
        arr.append({'label': one['name'], 'value': one['building_id']})
    return arr


def get_course_options():
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select * from course"
    cursor.execute(sql1)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    arr = []
    for one in result:
        arr.append({'label': one['name'], 'value': one['course_id']})
    return arr


def get_classroom_options():
    conn = get_a_conn()
    cursor = conn.cursor()
    sql1 = "select * from classroom"
    cursor.execute(sql1)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    arr = []
    for one in result:
        arr.append({'label': one['name'], 'value': one['classroom_id']})
    return arr
