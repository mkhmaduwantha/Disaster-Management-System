import unittest
import urllib

from flask_testing import LiveServerTestCase
from selenium import webdriver

from emas import create_app, db, bcrypt
from emas.models import User
from emas.config import Config

from selenium.webdriver.chrome.options import Options


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
        options = Options()
        options.binary_location = "/usr/bin/chromium-browser"
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(self.get_server_url())

        db.session.commit()
        db.drop_all()
        db.create_all()

        hashed_password = bcrypt.generate_password_hash("test").decode('utf-8')
        self.admin = User(title='Mr.', fname='admin', lname='admin', email='admin@gmail.com',
                          mobile_number='0000000000', password=hashed_password, user_type='Admin')
        self.test_user1 = User(title='Mr.', fname='test_user1', lname='user', email='test_user1@gmail.com',
                               mobile_number='0000000000', password=hashed_password, confirmed=True, user_type='User')
        self.test_user2 = User(title='Mr.', fname='test_user2', lname='user', email='test_user2@gmail.com',
                               mobile_number='0000000000', password=hashed_password, user_type='User')
        self.test_camp1 = User(title='Mr.', fname='test_camp1', lname='camp', email='test_camp1@gmail.com',
                               mobile_number='0000000000', password=hashed_password, user_type='Camp')
        self.test_camp2 = User(title='Mr.', fname='test_camp2', lname='camp', email='test_camp2@gmail.com',
                               mobile_number='0000000000', password=hashed_password, confirmed=True,  user_type='Camp')
        self.test_military1 = User(title='Mr.', fname='test_military1', lname='military', email='test_military1@gmail.com',
                                   mobile_number='0000000000', password=hashed_password, user_type='Military')
        self.test_military2 = User(title='Mr.', fname='test_military2', lname='military', email='test_military2@gmail.com',
                                   mobile_number='0000000000', password=hashed_password, confirmed=True, user_type='Military')

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
        response = urllib.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
