import unittest

from flask import abort, url_for, Flask
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from emas.config import Config
from flask_admin import Admin
from emas import create_app, db, bcrypt
from emas.models import User, Message, Address


class TestBase(TestCase):

    def create_app(self):
        app = create_app(config_class=Config)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
        )
        return app

    def setUp(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

        hashed_password = bcrypt.generate_password_hash("test").decode('utf-8')
        admin = User(title='Mr.', fname='admin', lname='admin', email='admin@gmail.com',
                     mobile_number='0000000000', password=hashed_password, user_type='Admin')
        test_user1 = User(title='Mr.', fname='test_user1', lname='user', email='test_user1@gmail.com',
                          mobile_number='0000000000', password=hashed_password, confirmed=True, user_type='User')
        test_user2 = User(title='Mr.', fname='test_user2', lname='user', email='test_user2@gmail.com',
                          mobile_number='0000000000', password=hashed_password, user_type='User')
        test_camp1 = User(title='Mr.', fname='test_camp1', lname='camp', email='test_camp1@gmail.com',
                          mobile_number='0000000000', password=hashed_password, user_type='Camp')
        test_camp2 = User(title='Mr.', fname='test_camp2', lname='camp', email='test_camp2@gmail.com',
                          mobile_number='0000000000', password=hashed_password, confirmed=True,  user_type='Camp')
        test_military1 = User(title='Mr.', fname='test_military1', lname='military', email='test_military1@gmail.com',
                              mobile_number='0000000000', password=hashed_password, user_type='Military')
        test_military2 = User(title='Mr.', fname='test_military2', lname='military', email='test_military2@gmail.com',
                              mobile_number='0000000000', password=hashed_password, confirmed=True, user_type='Military')

        db.session.add(admin)
        db.session.add(test_user1)
        db.session.add(test_user2)
        db.session.add(test_camp1)
        db.session.add(test_camp2)
        db.session.add(test_military1)
        db.session.add(test_military2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    def test_user_model(self):
        self.assertEqual(User.query.count(), 7)


class TestViews(TestBase):
    def test_homepage_view(self):
        response = self.client.get(url_for('home.home_page'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(url_for('users.login'))
        self.assertEqual(response.status_code, 200)

    def test_resgiter_view(self):
        response = self.client.get(url_for('users.register'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        target_url = url_for('users.logout')
        redirect_url = url_for('users.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_account_view(self):
        target_url = url_for('users.account')
        redirect_url = url_for('users.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_contact_view(self):
        target_url = url_for('users.account_contact')
        redirect_url = url_for('users.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_message_view(self):
        target_url = url_for('users.messages')
        redirect_url = url_for('users.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_profile_view(self):
        target_url = url_for('users.user', email='test@mail.com')
        redirect_url = url_for('users.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_send_message_view(self):
        target_url = url_for('users.notifications')
        redirect_url = url_for('users.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)

    def test_500_internal_server_error(self):
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
