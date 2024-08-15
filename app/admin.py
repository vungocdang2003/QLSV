from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db, dao
from app.stu import Year, Grade, Subject, Score, Student, User, UserRoleEnum
from flask_login import logout_user, current_user
from flask import redirect, request


admin = Admin(app=app, name='QUẢN TRỊ LỚP HỌC SINH', template_mode='bootstrap4')



class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyStudentView(AuthenticatedAdmin):
    column_list = ['MSHS', 'name', 'number', 'birth', 'gender', 'address', 'email']
    can_export = True
    column_searchable_list = ['MSHS', 'name']
    column_filters = ['MSHS', 'name']
    column_editable_list = ['name', 'number', 'birth', 'address', 'email']
    edit_modal = True



class MyYearView(AuthenticatedAdmin):
    column_list = ['id', 'name']
    can_export = True
    column_editable_list = ['name']
    edit_modal = True

class MySubjectView(AuthenticatedAdmin):
    column_list = ['id', 'name']
    can_export = True
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name']
    column_editable_list = ['name']
    edit_modal = True

class MyScoreView(AuthenticatedAdmin):
    column_list = ['id','students', 'fifteenTest1', 'fifteenTest2', 'forty_fiveTest1', 'forty_fiveTest2', 'finalTest']
    can_export = True
    column_searchable_list = ['id']
    column_filters = ['id']
    column_editable_list = ['students','fifteenTest1', 'fifteenTest2', 'forty_fiveTest1', 'forty_fiveTest2', 'finalTest']
    edit_modal = True


class MyGradeView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'quantity']
    can_export = True
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name']
    column_editable_list = ['name', 'quantity']
    edit_modal = True

class StatsView(AuthenticatedUser):
    @expose("/")
    def __index__(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()

        return redirect('/admin')


admin.add_view(MyYearView(Year, db.session))
admin.add_view(MyStudentView(Student, db.session))
admin.add_view(MyGradeView(Grade, db.session))
admin.add_view(MySubjectView(Subject, db.session))
admin.add_view(MyScoreView(Score, db.session))
admin.add_view(StatsView(name='Statics'))
admin.add_view(LogoutView(name='Logout'))
