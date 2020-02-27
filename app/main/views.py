from datetime import datetime

from . import main
from .forms import RegisterForm
from flask import session, flash, render_template, redirect, url_for, request, make_response, abort
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def register():
    flash('激活以后就可以顺利使用了！')
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        user = User(device_id=registerForm.device_id.data,
                    username=registerForm.username.data,
                    age=registerForm.age.data,
                    sex=registerForm.gender.data,
                    height=registerForm.height.data,
                    weight=registerForm.weight.data,
                    telephone=registerForm.telephone.data,
                    email=registerForm.email.data,
                    activation_time=datetime.utcnow()
                    )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Server Error.')
            return redirect(url_for('.register'))
        print(user)
        flash('设备激活成功，持续为您保驾护航。')
        return redirect(url_for('.register'))
    return render_template('register.html', registerForm=registerForm)


@main.route('/users/')
def users():
    userlist = User.query.all()
    for user in userlist:
        print(user.username)
        print(user.last_sync)
        print(user.heart_rate)
        print(user.email)
    return render_template('display.html', userlist=userlist)


@main.route('/upload/', methods=['POST'])
def upload_user_data():
    params = request.data.decode('utf-8').split(',')
    device_id = params[-1]
    user = User.query.filter_by(device_id=device_id).first()
    if not user:
        response = make_response('Invalid or Inactive device.')
        response.status_code = 400
        response.headers['Content-Type'] = 'text/plain'
        return response

    print(params)
    # status = params[0]
    # body_temperature = params[1]
    # heart_rate = params[2]
    # blood_oxygen = params[3]
    # latitude = params[4]
    # longitude = params[5]
    # locate_type = params[-2]
    user.status = params[0]
    user.body_temperature = params[1]
    user.heart_rate = params[2]
    user.blood_oxygen = params[3]
    user.latitude = params[4]
    user.longitude = params[5]
    user.locate_type = params[-2]
    user.last_sync = datetime.utcnow()
    print(user.status)
    print(user.body_temperature)
    print(user.heart_rate)
    print()

    db.session.add(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return 'sync error.'
    return 'sync success'


# Distributing user basic info to device according the device ID.
@main.route('/get_user_data/<string:device_id>')
def get_user_data(device_id):
    user = User.query.filter_by(device_id=device_id).first()
    if user is None:
        response = make_response('error')
        response.status_code = 404
        response.headers['Content-type'] = 'text/plain'
        response.headers['Charset'] = 'UTF-8'
        return response
    print(user.username)
    response = make_response(user.username + ','
                             + str(user.age) + ','
                             + str(user.sex) + ','
                             + str(user.height) + ','
                             + str(user.weight) + ','
                             + str(user.telephone)
                             )
    response.headers['Content-type'] = 'text/plain'
    response.headers['Charset'] = 'UTF-8'

    return response
