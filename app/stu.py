from sqlalchemy import Column, Integer, String, Double, ForeignKey, Enum, Boolean, Date
from datetime import datetime
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
import enum




class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/du5yfxccw/image/upload/v1704394415/m1ctsthqlha7sm6kcatu.png')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name

class Grade(db.Model):
    __tablename__ = 'grade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    quantity = Column(Integer)
    students = relationship('Student', backref='grade', lazy=True)

    # primaryjoin = 'Class.id == Student.class_id'
    def __str__(self):
        return self.name
#
#
#
class Subject(db.Model):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, autoincrement= True)
    name = Column(String(50), nullable=False, unique=True)
    students = relationship('Student', backref='subject', lazy=True)

    def __str__(self):
        return self.name


class Score(db.Model):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fifteenTest1 = Column(Double, nullable=False)
    fifteenTest2 = Column(Double, nullable=True)
    forty_fiveTest1 = Column(Double, nullable=False)
    forty_fiveTest2 = Column(Double, nullable=True)
    finalTest = Column(Double, nullable=False)
    students = relationship('Student', backref='score', lazy=True)


    def __str__(self):
        return self.id


class Year(db.Model):
    __tablename__ = 'year'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    students = relationship('Student', backref='year', lazy=True)


    def __str__(self):
        return self.name


class Student(db.Model):
    __tablename__ = 'student'
    MSHS = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=False)
    number = Column(String(30), nullable=False, unique=True)
    birth = Column(Date)
    gender = Column(String(30))
    address = Column(String(250), nullable=False)
    email = Column(String(50))
    image = Column(String(200))
    year_id = Column(Integer, ForeignKey('year.id'), nullable=False)
    grade_id = Column(Integer, ForeignKey('grade.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
    score_id = Column(Integer, ForeignKey('score.id'), nullable=False)

    def __str__(self):
        return self.name



if __name__ == '__main__':
    with app.app_context():
          # db.create_all()
        #1
        import hashlib
        u = User(name='Admin', username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)
        db.session.add(u)
        db.session.commit()

        y1 = Year(name='KÌ I--2023-2024')
        y2 = Year(name='KÌ II--2023-2024')

        db.session.add(y1)
        db.session.add(y2)
        db.session.commit()

        g1 = Grade(name='Khối 10', quantity='5')
        g2 = Grade(name='Khối 11', quantity='6')
        g3 = Grade(name='Khối 12', quantity='7')

        db.session.add(g1)
        db.session.add(g2)
        db.session.add(g3)
        db.session.commit()

        sub1 = Subject(name='Math')
        sub2 = Subject(name='Literature')
        sub3 = Subject(name='English')

        db.session.add(sub1)
        db.session.add(sub2)
        db.session.add(sub3)
        db.session.commit()
        # #
        sc1 = Score(fifteenTest1=8.0, fifteenTest2=8.0, forty_fiveTest1=8.0, forty_fiveTest2=8.0, finalTest=8.0)
        sc2 = Score(fifteenTest1=9.0, fifteenTest2=9.0, forty_fiveTest1=9.0, forty_fiveTest2=9.0, finalTest=9.0)
        sc3 = Score(fifteenTest1=8.5, fifteenTest2=8.5, forty_fiveTest1=9.0, forty_fiveTest2=9.5, finalTest=10.0)
        db.session.add(sc1)
        db.session.add(sc2)
        db.session.add(sc3)
        db.session.commit()


        s1 = Student(name='Nguyễn Thị Minh Anh', MSHS=101, number='1122334455', birth='2006-12-12',gender='Female', address='99 Pham Van Dong Street, Go Vap District, Ho Chi Minh City', email='minhanh@gmail.com', year_id=1, grade_id=1, subject_id=1, score_id=1,
                     image='https://res.cloudinary.com/du5yfxccw/image/upload/v1704394415/m1ctsthqlha7sm6kcatu.png')
        s2 = Student(name='Nguyễn Thị Ngọc Anh', MSHS=201, number='5566778899', birth='2008-12-01', gender='Female', address='100 Pham Van Dong Street, Go Vap District, Ho Chi Minh City', email='ngocanh@gmail.com', year_id=2, grade_id=2, subject_id=1, score_id=2,
                     image='https://res.cloudinary.com/du5yfxccw/image/upload/v1704394415/m1ctsthqlha7sm6kcatu.png')
        s3 = Student(name='Trần Văn Bình', MSHS=102, number='2233445566', birth='2007-12-25', gender='Male', address='101 Pham Van Dong Street, Go Vap District, Ho Chi Minh City', email='vanbinh@gmail.com', year_id=1, grade_id=1, subject_id=1, score_id=3,
                     image='https://res.cloudinary.com/du5yfxccw/image/upload/v1704394415/m1ctsthqlha7sm6kcatu.png')
        s4 = Student(name='Trần Văn Tính', MSHS=202, number='6677889911', birth='2008-12-04', gender='Male', address='102 Pham Van Dong Street, Go Vap District, Ho Chi Minh City', email='vantinh@gmail.com', year_id=2, grade_id=2, subject_id=1, score_id=1,
                     image='https://res.cloudinary.com/du5yfxccw/image/upload/v1704394415/m1ctsthqlha7sm6kcatu.png')
        s5 = Student(name='Đỗ Thị Bình An', MSHS=103, number='3344556677', birth='2008-10-30', gender='Female', address='103 Pham Van Dong Street, Go Vap District, Ho Chi Minh City', email='binhan@gmail.com', year_id=1, grade_id=1, subject_id=1, score_id=2,
                     image='https://res.cloudinary.com/du5yfxccw/image/upload/v1704394415/m1ctsthqlha7sm6kcatu.png')
        s6 = Student(name='Đỗ Thị Ngọc Bích', MSHS=203, number='7788991122', birth='2007-10-28', gender='Female', address='104 Pham Van Dong Street, Go Vap District, Ho Chi Minh City', email='ngocbich@gmail.com', year_id=2, grade_id=3, subject_id=1, score_id=3,
                     image='https://res.cloudinary.com/du5yfxccw/image/upload/v1704394415/m1ctsthqlha7sm6kcatu.png')

        db.session.add_all([s1, s2, s3, s4, s5, s6])
        db.session.commit()
