from datetime import date, datetime

from flask import render_template, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import desc

from app import app, socket, db
from app.forms import LoginForm
from app.models import User, Userdata

from workers import hassu, canlogin, generate_rnd


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and not current_user.is_authenticated:

        username = str(request.form['username'])
        password = str(request.form['password'])
        if request.form['remember_me']:
            remember_me = True
        else:
            remember_me = False

        u = User.query.filter_by(username=username).first()

        if u and u.check_password(password):
            login_user(u, remember_me)
            u.last_activity = datetime.now()
            db.session.commit()

        if u.is_superuser:
            users = User.query.order_by(User.username).all()
            return render_template('index2.html', title='Index', users=users)

        else:
            return redirect('/')

    elif current_user.is_authenticated and current_user.is_superuser:
        users = User.query.order_by(User.username).all()
        #userdata = Userdata.query.all()

        '''for user in users:
            print('USERNAME: ', user.username)
            print('FULLNAME: ', user.userdata.fullname)
            print('ADDRESS: ', user.userdata.address)'''

        return render_template('index2.html', title='Index', users=users)

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
        user.email = generate_rnd(12)
        user.set_password(password)
        user.is_superuser = True
        user.joined = date.today()
        user.last_activity = datetime.now()

        userdata = Userdata(userid=user.id)

        userdata.photo_path = '/static/img/avatars/adminavatar.png'
        userdata.fullname = generate_rnd(12)
        userdata.joined = datetime.now()
        userdata.address = generate_rnd(12)
        userdata.user=user.id
        userdata.mmn = generate_rnd(12)

        db.session.add(user)
        db.session.commit()

    return redirect('/')


#websocket event dispatcher
@socket.on('newmessage')
def newmessage(data):

    sid = request.sid


    #request for loginmodal - DONE
    if data['event'] == 201 and not current_user.is_authenticated:
        loginform = LoginForm()
        mess = {}
        mess['event'] = 101
        mess['htm'] = render_template('loginmodal.html', title='Belépés', loginform = loginform)
        socket.emit('newmessage', mess, room=sid)
        return True


    #request for error modal
    if data['event'] == 209:
        mess = {}
        mess['event'] = 109
        mess['htm'] = render_template('errormessage.html', message=data['message'])
        socket.emit('newmessage', mess, room=sid)
        return True


    #loginattempt - DONE
    if data['event'] == 221 and not current_user.is_authenticated:
        if canlogin(data):
            mess = {}
            mess['event'] = 121
            socket.emit('newmessage', mess, room=sid)
        else:
            mess = {}
            mess['event'] = 109
            mess['htm'] = render_template('errormessage.html', message='Rossz felhasználónév vagy jelszó!')
            socket.emit('newmessage', mess, room=sid)
        return True


#-------------------------------------------- dev ops --------------------------------------


    #request for avatarselector
    if data['event'] == 401 and current_user.is_superuser:
        mess = {}
        mess['event'] = 301
        mess['htm'] = render_template('avatars.html')
        socket.emit('newmessage', mess, room=sid)
        return True

