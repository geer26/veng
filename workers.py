import re
import string
from datetime import timedelta, date, datetime
from random import random, SystemRandom, randrange

from app import db
from app.models import User


def validate_email(email):
    pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return (re.search(pattern, email))


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def hassu():
    return False

def canlogin(data):
    username = str(data['username'])
    password = str(data['password'])
    u = User.query.filter_by(username=username).first()
    if not u: return False
    if not u.check_password(password): return False
    return True

def generate_rnd(N):
    return ''.join(SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N))


def userregister(data):

    if  not validate_email(data['email']):
        #Wrong email format
        return 1
    try:
        phone =int(data['phone'])
    except:
        #wrong phone number
        return 2

    user = User()

    #Randomized!
    user.username = generate_rnd(5)
    # Randomized!
    user.set_password(generate_rnd(8))
    # Randomized!
    user.uuid = generate_rnd(10)
    user.email = data['email']
    user.is_superuser = False
    user.photo_path = data['photo_path']
    # Randomized!
    user.dob = random_date(date(1980, 1, 1), date(2000, 1, 1))
    user.joined = datetime.today()
    user.association = data['associaton']
    # Randomized!
    user.lic_type = generate_rnd(4)
    user.license_no = data['lic_no']
    if data['gender']:
        #Woman
        user.gender = 2
    else:
        #man
        user.gender = 1
    user.gender = 0
    user.mmn = data['mmn']
    user.address = data['address']
    user.phone_no = data['phone']

    db.session.add(user)
    db.session.commit()

    return 0
