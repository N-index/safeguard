from datetime import datetime
from . import main
from .forms import RegisterForm, SearchForm
from flask import flash, render_template, redirect, url_for, request, make_response, abort, jsonify
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def register():
    flash('激活使用。')
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        r_user = User(device_id=registerForm.device_id.data,
                      username=registerForm.username.data,
                      age=registerForm.age.data,
                      sex=registerForm.gender.data,
                      height=registerForm.height.data,
                      weight=registerForm.weight.data,
                      telephone=registerForm.telephone.data,
                      email=registerForm.email.data,
                      activation_time=datetime.utcnow()
                      )
        db.session.add(r_user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Server Error.')
            return redirect(url_for('.register'))
        flash('设备激活成功，持续为您保驾护航。')
        return redirect(url_for('.register'))
    return render_template('register.html', registerForm=registerForm)


@main.route('/users/', methods=['GET', 'POST'])
def users():
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        return redirect(url_for('main.user', username=searchForm.username.data))

    userlist = User.query.order_by(User.activation_time.desc()).all()

    return render_template('display.html', userlist=userlist, searchForm=searchForm)


@main.route('/user/<username>/', methods=['GET', 'POST'])
def user(username):
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        searched_user = User.query.filter_by(username=searchForm.username.data).first()
        if searched_user is None:
            flash('查无此人')
            return redirect(url_for('main.users'))
        return render_template('display.html', userlist=[searched_user], searchForm=searchForm)
    searched_user = User.query.filter_by(username=username).first()

    if searched_user is None:
        flash('查无此人')
        return redirect(url_for('main.users'))
    return render_template('display.html', userlist=[searched_user], searchForm=searchForm)


@main.route('/test/', methods=['POST'])
def test():
    params = request.data.decode('utf-8').split(',')
    print(params)
    return 'success'


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
    # 纬度
    user.latitude = params[5]
    # 经度
    user.longitude = params[4]
    user.locate_type = params[-2]
    user.last_sync = datetime.utcnow()

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


@main.route('/get_device_id/', methods=['GET'])
def get_id():
    res = []
    for _ in User.query.all():
        res.append(_.device_id)
    return jsonify({
        'device_id': res
    })


@main.route('/profile/<device_id>')
def profile(device_id):
    print(device_id)
    user = User.query.filter_by(device_id=device_id).first()
    if user is None:
        return render_template('404.html',message='用户不存在。')
    return render_template('profile.html', userlist=[user])
