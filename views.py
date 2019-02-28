from flask import request, make_response, jsonify
from flask.views import MethodView

from app import db
from models import UserLogin, UserInfo, Tokens
from funcs_for_tokens import extract_from_form, generate_auth_token, validate_token


class UserRegistration(MethodView):

    def get(self):
        return 'It is an registration page. [GET]'

    def post(self):
        if not UserLogin.query.filter_by(login=request.form['login']).first():
            try:
                user_login = UserLogin(password_hash=request.form['password'], login=request.form['login'])
            except KeyError:
                return 'Login and password are necessary!', 400
            db.session.add(user_login)
            db.session.commit()
            user_info = UserInfo(**extract_from_form(request.form, ('name', 'surname', 'age')),
                                 user_login_id=user_login.user_id)
            db.session.add(user_info)
            db.session.commit()
            return 'Registration is successful'
        else:
            return 'Please try again, not enough information of your login already exist'


class UserInformation(MethodView):
    @validate_token
    def get(self):
        token_value = request.headers.environ['HTTP_AUTHORIZATION'].split()[-1]
        user = Tokens.query.filter_by(token=token_value).first()
        if user:
            user_login = UserLogin.query.filter_by(login=user.user_login).first()
            responseObject = {
                'Name': user_login.info.name,
                'Surname': user_login.info.surname,
                'Age': user_login.info.age
            }
            return make_response(jsonify(responseObject)), 200
        else:
            return 'Something went wrong'

    @validate_token
    def put(self):
        token_value = request.headers.environ['HTTP_AUTHORIZATION'].split()[-1]
        user_token = Tokens.query.filter_by(token=token_value).first()
        user_info = UserInfo.query.filter_by(user_id=user_token.user_id).first()
        user_info.partial_update(request.form)
        db.session.commit()
        return 'Data is updated', 200


class LoginAPI(MethodView):
    def post(self):
        try:
            user = UserLogin.query.filter_by(login=request.form['login']).first()
            if user is None or not user.check_password(request.form['password']):
                raise Exception
            else:
                auth_token = generate_auth_token(user.login)
                if auth_token:
                    responseObject = {
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500

    def get(self):
        return 'This is login page, enter your credentials'


class Logout(MethodView):
    @validate_token
    def post(self):
        try:
            token_value = request.headers.environ['HTTP_AUTHORIZATION'].split()[-1]
            user_token = Tokens.query.filter_by(token=token_value).first()
            db.session.delete(user_token)
            db.session.commit()
            return 'You are logged out'
        except Exception as e:
            return e
