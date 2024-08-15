import math
from flask import render_template, request, redirect
from flask_login import login_user, logout_user
import dao
from app import app, login


@app.route('/')
def index():
    kw = request.args.get('kw')
    year_id = request.args.get('year_id')
    page = request.args.get('page')
    Years = dao.load_years()
    Grades = dao.load_grades()
    Subjects = dao.load_subjects()
    Scores = dao.load_scores()
    students = dao.load_students(kw, year_id)
    countstu = dao.count_students()

    return render_template('index.html', years=Years, students=students, grades=Grades, scores=Scores,
                           pages=math.ceil(countstu / app.config['PAGE_SIZE']))


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password, avatar=request.files.get('avatar'))
            except Exception as ex:
                print(str(ex))
                err_msg = 'Hệ thống đang bị lỗi!'
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('/register.html', err_msg=err_msg)


@app.route("/login", methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)

    return render_template('login.html')


@app.route('/logout')
def process_user_logout():
    logout_user()
    return redirect("/login")


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
