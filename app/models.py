from datetime import datetime

from app import login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin,db.Model):
    #__tablename__ = 'u'
    id = db.Column(db.Integer, primary_key=True)
    userdata = db.relationship('Userdata', backref='_user', cascade='all,delete', uselist=False)

    uuid = db.Column(db.String(12), index=True)
    username = db.Column(db.String(12), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    is_superuser = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def compare_passwords(self, password1, password2):
        return generate_password_hash(password1) == generate_password_hash(password2)


class Userdata(db.Model):
    #__tablename__ = 'udata'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

    photo_path = db.Column(db.String(60))
    fullname = db.Column(db.String(60))
    dob = db.Column(db.DateTime)  #Date Of Birth
    pob = db.Column(db.String(60))  #PlaceOfBirth
    joined = db.Column(db.DateTime, default=datetime.now())
    association = db.Column(db.String(60))
    license_no = db.Column(db.String(60))
    gender = db.Column(db.Integer)
    mmn = db.Column(db.String(60)) #MothersMaidenNAme
    address = db.Column(db.String(120))
    phone_no = db.Column(db.String(25))
    lic_type = db.Column(db.Integer)

    def __repr__(self):
        return str(self.fullname)