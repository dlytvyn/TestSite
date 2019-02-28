import datetime
import hashlib

from flask import request, abort

from app import db
from models import Tokens, UserLogin


def validate_token(func):
    def wrapper(*args, **kwargs):
        if validate_auth_token(request.headers.environ['HTTP_AUTHORIZATION']):
            return func(*args, *kwargs)
        else:
            abort(403)
    return wrapper


def extract_from_form(form, struct):
    return {elem: form[elem] for elem in struct if form.get(elem) is not None}


def generate_auth_token(user_login):
    try:
        token_info = user_login + datetime.datetime.utcnow().isoformat()
        token = hashlib.sha224(token_info.encode('utf-8')).hexdigest()
        user_token = Tokens(user_login=user_login,
                            token=token,
                            user_id=UserLogin.query.filter_by(login=request.form['login']).first().user_id)
        db.session.add(user_token)
        db.session.commit()
        return token
    except:
        abort(403)


def validate_auth_token(auth_token):
    token_value = auth_token.split()[-1]
    user = Tokens.query.filter_by(token=token_value).first()
    return user
