from functools import wraps
from flask import redirect, url_for, request
from flask_login import current_user


def only_confirmed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            return redirect(url_for('auth.unconfirmed', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
