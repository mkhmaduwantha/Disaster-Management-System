from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from emas import db, login_manager
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from flask import current_app
import json
from time import time
from itsdangerous import URLSafeTimedSerializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# basic_user


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # details of the user
    title = db.Column(db.String(255), nullable=False)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255, collation='NOCASE'),
                      nullable=False, unique=True)
    mobile_number = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(255), nullable=False, server_default='')
    # profile image
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    # for displaying last seen
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # to find the user roles
    roles = db.relationship('Role', secondary='user_roles')
    # user type ready for inheritance
    user_type = db.Column(db.String(32), nullable=False, server_default='user')
    # for messaging funciton
    messages_sent = db.relationship(
        'Message', foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    messages_received = db.relationship(
        'Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    # showing notifications badge
    notifications = db.relationship(
        'Notification', backref='user', lazy='dynamic')
    # email confirmation
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    # contact information
    # for home user
    home_address = db.relationship(
        'Address', foreign_keys='Address.user_id',  lazy='dynamic')
    home_number = db.Column(db.String(12))
    # for military
    designation = db.Column(db.String(255))
    office_address = db.relationship(
        'Address', foreign_keys='Address.user_id',  lazy='dynamic')
    office_number = db.Column(db.String(12))
    # for camps
    total_number = db.Column(db.String(255))
    occupied_number = db.Column(db.String(255))
    camp_name = db.Column(db.String(255))
    camp_number = db.Column(db.String(12))
    camp_address = db.relationship(
        'Address', foreign_keys='Address.user_id', backref='user_address', lazy='dynamic')
    camp_needs = db.Column(db.String(255))

    # generatin reset token for password
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def generate_confirmation_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    # messages
    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()
    # notificaton

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n
    # verifying   password reset token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.fname}','{self.lname}', '{self.email}', '{self.image_file}','{self.confirmed}','{self.confirmed_on}')"


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    line_one = db.Column(db.String(255), nullable=False)
    line_two = db.Column(db.String(255), nullable=True)
    province = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Role('{self.line_one}','{self.line_two}','{self.province}','{self.district}','{self.city}','{self.postal_code}')"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"Role('{self.name}')"


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

