from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class UserLogin(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    info = db.relationship('UserInfo', back_populates='creds', uselist=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_password(kwargs.pop('password_hash'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Login = {}, password = {}>'.format(self.login, self.password_hash)


class UserInfo(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_login_id = db.Column(db.Integer, db.ForeignKey('user_login.user_id'))
    creds = db.relationship('UserLogin', back_populates='info', uselist=False)
    name = db.Column(db.String(64), index=True, unique=False)
    surname = db.Column(db.String(64), index=True, unique=False)
    age = db.Column(db.Integer)

    def partial_update(self, new_data):
        struct = ('name', 'surname', 'age')
        for elem in struct:
            if new_data.get(elem) is not None:
                setattr(self, elem, new_data[elem])

    def __repr__(self):
        return 'Name = {}, Surname = {}, Age = {}'.format(self.name, self.surname, self.age)


class Tokens(db.Model):
    token_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), index=True, unique=True)
    user_login = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer, index=True, unique=True)


db.create_all()
