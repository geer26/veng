from datetime import date, datetime

from flask import render_template, redirect, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, socket, db, qr
from app.forms import LoginForm
from app.models import User

from workers import hassu, canlogin, generate_rnd, userregister


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and not current_user.is_authenticated:

        username = str(request.form['username'])
        password = str(request.form['password'])
        if request.form['remember_me'] and request.form['remember_me'] == 'y':
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
        users = User.query.order_by(User.id).all()

        return render_template('index2.html', title='Index', users=users)

    else:
        return render_template('index2.html', title='Index')


@app.route('/user/<uuid>')
def userdata(uuid):
    user = User.query.get(uuid=uuid)
    return render_template('userdata.html', user=user)


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
        user.fullname = 'Administrator'
        user.address = generate_rnd(12)
        user.association = generate_rnd(12)
        user.mmn = generate_rnd(12)
        user.photo_path = '/static/img/avatars/adminavatar.png'


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


    #delete user - DONE
    if data['event'] == 222 and current_user.is_superuser:
        u = User.query.get(int(data['id']))
        if u:
            db.session.delete(u)
            db.session.commit()
            mess = {}
            mess['event'] = 122
            mess['id'] = int(data['id'])
            socket.emit('newmessage', mess, room=sid)
            return True
        else:
            #user do not exists
            return False


    #register for new user
    if data['event'] == 231 and current_user.is_superuser:
        r = userregister(data)
        if r == 1:
            mess = {}
            mess['event'] = 109
            mess['htm'] = render_template('errormessage.html', message='Rossz email cím formátum!')
            socket.emit('newmessage', mess, room=sid)
            return False

        elif r == 2:
            mess = {}
            mess['event'] = 109
            mess['htm'] = render_template('errormessage.html', message='Rossz telefonszám formátum!')
            socket.emit('newmessage', mess, room=sid)
            return False

        elif r == 0:
            mess= {}
            mess['event'] = 131
            socket.emit('newmessage', mess, room=sid)
            return True


    #request for usertable refreshment
    if data['event'] == 251 and current_user.is_authenticated:
        users = User.query.order_by(User.username).all()
        mess = {}
        mess['event'] = 151
        mess['htm'] = render_template('admin_users.html', users=users)
        socket.emit('newmessage', mess, room=sid)
        return True


    #request for QR
    if data['event'] == 261 and current_user.is_superuser:
        mess = {}
        mess['event']=161
        mess['htm'] = render_template('qrcode.html', url=str(data['domain'])+'/'+str(data['uuid']))
        print(mess['htm'])
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


    #request for adduser modal
    if data['event'] == 402 and current_user.is_superuser:
        mess = {}
        mess['event'] = 302
        mess['htm'] = render_template('adduser_modal.html')
        socket.emit('newmessage', mess, room=sid)
        return True
