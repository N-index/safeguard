from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

# from ..models import Permi


def anonymous_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_anonymous:
                flash('用户已经登录')
                return redirect(url_for('main.profile', device_id=current_user.device_id))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
