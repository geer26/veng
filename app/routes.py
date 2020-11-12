from datetime import date, datetime

from flask import render_template, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import desc

from app import app, socket, db
from app.forms import LoginForm, SignupForm
from app.models import User, Userdata


#logs in user - DONE
from workers import hassu


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and not current_user.is_authenticated:

        username = request.form['username']
        password = request.form['password']
        if request.form['remember_me'] == 'y':
            remember_me = True
        else:
            remember_me = False

        print(username)
        print(password)
        print(remember_me)

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember_me)
            user.last_activity = datetime.now()
            db.session.commit()

        return redirect('/')
    else:
        return render_template('index2.html', title='Index')


#logs out user - DONE
@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.last_activity = datetime.now()
    db.session.commit()
    logout_user()
    return redirect('/')


#add superuser - DONE
@app.route('/addsu/<suname>/<password>')
def addsu(suname, password):
    #eg. https://example.com/examplesuname/example1Password!2
    if not hassu():

        user = User()

        user.username = suname
        user.email = 'none@none.no'
        user.set_password(password)
        user.is_superuser = True
        user.joined = date.today()
        user.last_activity = datetime.now()

        db.session.add(user)
        db.session.commit()

    return redirect('/')


#websocket event dispatcher
@socket.on('newmessage')
def newmessage(data):

    sid = request.sid


    #request for loginmodal
    if data['event'] == 201:
        loginform = LoginForm()
        mess = {}
        mess['event'] = 101
        mess['htm'] = render_template('loginmodal.html', title='Belépés', loginform = loginform)
        socket.emit('newmessage', mess, room=sid)
        return True

    #incoming request for error message with message - DONE
    if data['event'] == 291:
        mess = {}
        mess['event'] = 191
        mess['htm'] = render_template('errormessage.html', message=data['message'])
        socket.emit('newmessage', mess, room=sid)
        return True
