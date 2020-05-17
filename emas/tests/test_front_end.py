import unittest
import urllib
import time
from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver

from emas import create_app, db, bcrypt
from emas.models import User
from emas.config import Config

from selenium.webdriver.chrome.options import Options

hashed_password = bcrypt.generate_password_hash("test").decode('utf-8')

admin_title = "Mr."
admin_fname = "admin"
admin_lname = "admin"
admin_email = "admin@email.com"
admin_mobile_number = "0000000000"
admin_password = hashed_password
admin_user_type = "Admin"

test_user1_title = "Mr."
test_user1_fname = "test_user1"
test_user1_lname = "test_user1"
test_user1_email = "test_user1@email.com"
test_user1_mobile_number = "0000000000"
test_user1_password = hashed_password
test_user1_user_type = "User"

test_user2_title = "Mr."
test_user2_fname = "test_user2"
test_user2_lname = "test_user2"
test_user2_email = "test_user2@email.com"
test_user2_mobile_number = "0000000000"
test_user2_password = hashed_password
test_user2_user_type = "User"

test_camp1_title = "Mr."
test_camp1_fname = "test_camp1"
test_camp1_lname = "test_camp1"
test_camp1_email = "test_camp1@email.com"
test_camp1_mobile_number = "0000000000"
test_camp1_password = hashed_password
test_camp1_user_type = "Camp"

test_camp2_title = "Mr."
test_camp2_fname = "test_camp2"
test_camp2_lname = "test_camp2"
test_camp2_email = "test_camp2@email.com"
test_camp2_mobile_number = "0000000000"
test_camp2_password = hashed_password
test_camp2_usertype = "Camp"

test_military1_title = "Mr."
test_military1_fname = "test_military1"
test_military1_lname = "test_military1"
test_military1_email = "test_military1@email.com"
test_military1_mobile_number = "0000000000"
test_military1_password = hashed_password
test_military1_user_type = "Military"

test_military2_title = "Mr."
test_military2_fname = "test_military2"
test_military2_lname = "test_military2"
test_military2_email = "test_military2@email.com"
test_military2_mobile_number = "0000000000"
test_military2_password = hashed_password
test_military2_usertype = "Military"

class TestBase(LiveServerTestCase):

    def create_app(self):
        app = create_app(config_class=Config)
        app.config.update(
            # Specify the test database
            SQLALCHEMY_DATABASE_URI='sqlite:///test2.db',
            # Change the port that the liveserver listens on
            LIVESERVER_PORT=8943
        )
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())

        db.session.commit()
        db.drop_all()
        db.create_all()

        self.admin = User(title=admin_title, fname=admin_fname, lname=admin_lname, email = admin_email,
                          mobile_number=admin_mobile_number, password=admin_password, user_type=admin_user_type)
        self.test_user1 = User(title=test_user1_title, fname=test_user1_fname, lname=test_user1_lname, email = test_user1_email,
                          mobile_number=test_user1_mobile_number, password=test_user1_password, user_type=test_user1_user_type)
        self.test_user2 = User(title=test_user2_title, fname=test_user2_fname, lname=test_user2_lname, email = test_user2_email,
                          mobile_number=test_user2_mobile_number, password=test_user2_password, user_type=test_user2_user_type)
        self.test_camp1 = User(title=test_camp1_title, fname=test_camp1_fname, lname=test_camp1_lname, email = test_camp1_email,
                          mobile_number=test_camp1_mobile_number, password=test_camp1_password, user_type=test_camp1_user_type)
        self.test_camp2 = User(title=test_camp2_title, fname=test_camp2_fname, lname=test_camp2_lname, email = test_camp2_email,
                          mobile_number=test_camp2_mobile_number, password=test_camp2_password, user_type=test_camp2_user_type)
        self.test_military1 = User(title=test_military1_title, fname=test_military1_fname, lname=test_military1_lname, email = test_military1_email,
                          mobile_number=test_military1_mobile_number, password=test_military1_password, user_type=test_military1_user_type)
        self.test_military2 = User(title=test_military2_title, fname=test_military2_fname, lname=test_military2_lname, email = test_military2_email,
                          mobile_number=test_military2_mobile_number, password=test_military2_password, user_type=test_military2_user_type)

        db.session.add(self.admin)
        db.session.add(self.test_user1)
        db.session.add(self.test_user2)
        db.session.add(self.test_camp1)
        db.session.add(self.test_camp2)
        db.session.add(self.test_military1)
        db.session.add(self.test_military2)
        db.session.commit()

    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


class TestRegistration(TestBase):
    def test_registration(self):
        self.driver.find_element_by_id("register_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("title").send_keys(test_user1_title)
        self.driver.find_element_by_id("fname").send_keys(test_user1_fname)
        self.driver.find_element_by_id("lname").send_keys(test_user1_lname)
        self.driver.find_element_by_id("email").send_keys(test_user1_email)
        self.driver.find_element_by_id("password").send_keys(test_user1_password)
        self.driver.find_element_by_id("confirm_password").send_keys(test_user1_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(1)

        assert url_for('users.login') in self.driver.current_url

if __name__ == '__main__':
    unittest.main()
