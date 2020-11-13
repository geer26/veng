from app.models import User


def hassu():
    return False

def canlogin(data):
    username = str(data['username'])
    password = str(data['password'])
    u = User.query.filter_by(username=username).all()
    if not u: return False
    if not u.check_password(password): return False
    return True