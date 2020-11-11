from datetime import datetime

from app import login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    is_superuser = db.Column(db.Boolean, default=False)
    last_activity = db.Column(db.DateTime)
    userdata= db.relationship('userdata', backref='_user', cascade = 'all,delete')

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def compare_passwords(self, password1, password2):
        return generate_password_hash(password1) == generate_password_hash(password2)

class Userdata(db.Model):
    __tablename__ = 'userdata'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    photo_path = db.Column(db.String(60))
    fullname = db.Column(db.String(60))
    dob = db.Column(db.DateTime)  #Date Of Birth
    pob = db.Column(db.String(60))  #PlaceOfBirth
    joined = db.Column(db.DateTime)
    association = db.Column(db.String(60))
    license_no = db.Column(db.String(60))
    gender = db.Column(db.Integer)
    mmn = db.Column(db.String(60)) #MothersMaidenNAme
    address = db.Column(db.String(120))
    phone_no = db.Column(db.String(25))
    lic_type = db.Column(db.Integer)

    def __repr__(self):
        return str(self.fullname)

'''class Pocket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(120), default='')
    balance = db.Column(db.Integer, default=0)
    last_change = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transfers = db.relationship('Transfer', backref = '_pocket', cascade = 'all,delete')

    def __repr__(self):
        return str(self.id)+'_'+str(self.name)


class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, default=0)
    detail = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    pocket = db.Column(db.Integer, db.ForeignKey('pocket.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return str(self.id)+'_'+str(self.amount)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    type = db.Column(db.Integer, default=1)
    hidden = db.Column(db.Boolean, default=False)
    last_active = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # THINK OF CASCADING!!!
    transfer = db.relationship('Transfer', backref='_category')

    def __repr__(self):
        return self.name'''