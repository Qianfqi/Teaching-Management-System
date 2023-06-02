import hashlib
import time
from flask import Blueprint, render_template, request, redirect, session, json, current_app as app
from tools import *
from public import r

account = Blueprint('account', __name__)


@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.get_data()
    j_data = json.loads(data)
    conn = get_a_conn()
    cursor = conn.cursor()
    level = j_data['level']
    account = j_data['account']
    password = j_data['password']
    if level == 0:
        sql1 = f"select * from student where account='{account}'"
    elif level == 1:
        sql1 = f"select * from teacher where account='{account}'"
    else:
        sql1 = f"select * from admin where account='{account}'"
    cursor.execute(sql1)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        if result['password'] == password:
            if level == 0:
                session['uid'] = result['student_id']
            elif level == 1:
                session['uid'] = result['teacher_id']
            else:
                session['uid'] = result['admin_id']
            session['name'] = result['name']
            session['level'] = level
            session['logged_in'] = True
            print(session)
            return r({'is_login': 0}, 0, '欢迎登录：' + result['name'])
    return r({}, 1, '账号密码错误')


# 首页
@account.route('/index', methods=['GET'])
def index():
    data = {}
    return render_template('index.html', **data)
    pass


# 修改密码
@account.route('/account/editpwd', methods=['GET', 'POST'])
def editpwd():
    if request.method == 'GET':
        return render_template('/account/editpwd.html')
    data = request.get_data()
    j_data = json.loads(data)
    if j_data['pwd'] != j_data['pwd2']:
        return r({}, 1, '两次输入的密码不一致')
    local_salt = app.config.get("SALT")
    salt = hashlib.md5(str(time.time()).encode(encoding='UTF-8')).hexdigest()
    temp = j_data['pwd'] + local_salt + salt
    pwd = hashlib.md5(temp.encode(encoding='UTF-8')).hexdigest()
    db.session.query(Admin).filter(Admin.id == session['uid']).update({"salt": salt, 'password': pwd})
    status = db.session.commit()
    return r({'salt': salt, 'status': status}, 0)


# 退出登录
@account.route('/account/logout', methods=['GET'])
def logout():
    session.clear()  # 删除所有
    return redirect('/login')

