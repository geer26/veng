import string
from random import random, SystemRandom

from app.models import User


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
