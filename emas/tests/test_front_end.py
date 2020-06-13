import unittest
import urllib
import time
from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from emas import create_app, db, bcrypt
from emas.models import User
from emas.config import Config

from selenium.webdriver.chrome.options import Options

admin_title = "Mr."
admin_fname = "admin"
admin_lname = "admin"
admin_email = "admin@email.com"
admin_mobile_number = "0000000000"
admin_password = "test"
admin_user_type = "Admin"

test_user1_title = "Mr."
test_user1_fname = "test_user1"
test_user1_lname = "test_user1"
test_user1_email = "test_user1@email.com"
test_user1_mobile_number = "0000000000"
test_user1_password = "test"
test_user1_user_type = "User"

test_user2_title = "Mr."
test_user2_fname = "test_user2"
test_user2_lname = "test_user2"
test_user2_email = "test_user2@email.com"
test_user2_mobile_number = "0000000000"
test_user2_password = "test2"
test_user2_user_type = "User"

test_camp1_title = "Mr."
test_camp1_fname = "test_camp1"
test_camp1_lname = "test_camp1"
test_camp1_email = "test_camp1@email.com"
test_camp1_mobile_number = "0000000000"
test_camp1_password = "test"
test_camp1_user_type = "Camp"

test_camp2_title = "Mr."
test_camp2_fname = "test_camp2"
test_camp2_lname = "test_camp2"
test_camp2_email = "test_camp2@email.com"
test_camp2_mobile_number = "0000000000"
test_camp2_password = "test"
test_camp2_user_type = "Camp"

test_military1_title = "Mr."
test_military1_fname = "test_military1"
test_military1_lname = "test_military1"
test_military1_email = "test_military1@email.com"
test_military1_mobile_number = "0000000000"
test_military1_password = "test"
test_military1_user_type = "Military"

test_military2_title = "Mr."
test_military2_fname = "test_military2"
test_military2_lname = "test_military2"
test_military2_email = "test_military2@email.com"
test_military2_mobile_number = "0000000000"
test_military2_password = "test"
test_military2_user_type = "Military"

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
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.get_server_url())
        
        db.session.commit()
        db.drop_all()
        db.create_all()
        hashed_password = bcrypt.generate_password_hash("test2")
        self.admin = User(title=admin_title, fname=admin_fname, lname=admin_lname, email = admin_email,
                          mobile_number=admin_mobile_number, password=hashed_password, user_type=admin_user_type, confirmed = True)
        
        self.test_user2 = User(title=test_user2_title, fname=test_user2_fname, lname=test_user2_lname, email = test_user2_email,
                          mobile_number=test_user2_mobile_number, password=hashed_password, user_type=test_user2_user_type, confirmed = True)

        self.test_camp2 = User(title=test_camp2_title, fname=test_camp2_fname, lname=test_camp2_lname, email = test_camp2_email,
                          mobile_number=test_camp2_mobile_number, password=hashed_password, user_type=test_camp2_user_type, confirmed = True)
        
        self.test_military2 = User(title=test_military2_title, fname=test_military2_fname, lname=test_military2_lname, email = test_military2_email,
                          mobile_number=test_military2_mobile_number, password=hashed_password, user_type=test_military2_user_type, confirmed = True)
        

        db.session.add(self.admin)
        db.session.add(self.test_user2)
        db.session.add(self.test_camp2)
        db.session.add(self.test_military2)
        db.session.commit()

    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

class TestRegistration(TestBase):
    def test_registration(self):
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("profile_link"))
        hover.perform()
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("user_link"))
        hover.perform()
        element = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.ID, "register_link")))
        element.click()
        time.sleep(1)  

        self.driver.find_element_by_id("title").send_keys(test_user1_title)
        self.driver.find_element_by_id("fname").send_keys(test_user1_fname)
        self.driver.find_element_by_id("lname").send_keys(test_user1_lname)
        self.driver.find_element_by_id("email").send_keys(test_user1_email)
        self.driver.find_element_by_id("password").send_keys(test_user1_password)
        self.driver.find_element_by_id("mobile_number").send_keys(test_user1_mobile_number)
        self.driver.find_element_by_id("confirm_password").send_keys(test_user1_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(1)

        assert url_for('users.login') in self.driver.current_url

        success_message = self.driver.find_element_by_id("alert").text
        assert "Account created for" in success_message

        #self.assertEqual(User.query.count(),1)

    def test_registration_invalid_email(self):

        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("profile_link"))
        hover.perform()
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("user_link"))
        hover.perform()
        element = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.ID, "register_link")))
        element.click()
        time.sleep(1)   

        self.driver.find_element_by_id("title").send_keys(test_user1_title)
        self.driver.find_element_by_id("fname").send_keys(test_user1_fname)
        self.driver.find_element_by_id("lname").send_keys(test_user1_lname)
        self.driver.find_element_by_id("email").send_keys("invalid email")
        self.driver.find_element_by_id("password").send_keys(test_user1_password)
        self.driver.find_element_by_id("mobile_number").send_keys(test_user1_mobile_number)
        self.driver.find_element_by_id("confirm_password").send_keys(test_user1_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(5)

        error_message = self.driver.find_element_by_id("error_email").text
        assert "Invalid email address" in error_message


    def test_registration_confirm_password(self):

        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("profile_link"))
        hover.perform()
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("user_link"))
        hover.perform()
        element = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.ID, "register_link")))
        element.click()
        time.sleep(1)   


        self.driver.find_element_by_id("title").send_keys(test_user1_title)
        self.driver.find_element_by_id("fname").send_keys(test_user1_fname)
        self.driver.find_element_by_id("lname").send_keys(test_user1_lname)
        self.driver.find_element_by_id("email").send_keys(test_user1_email)
        self.driver.find_element_by_id("password").send_keys(test_user1_password)
        self.driver.find_element_by_id("confirm_password").send_keys("not-matching-password")
        self.driver.find_element_by_id("mobile_number").send_keys(test_user1_mobile_number)

        self.driver.find_element_by_id("submit").click()
        time.sleep(5)

        error_message = self.driver.find_element_by_id("error_password").text
        assert "Field must be equal to password." in error_message

class TestLogin(TestBase):
    def test_login(self):
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("profile_link"))
        hover.perform()
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("user_link"))
        hover.perform()
        element = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.ID, "login_link")))
        element.click()
        time.sleep(1)  
        self.driver.find_element_by_id("email").send_keys(test_user2_email)
        self.driver.find_element_by_id("password").send_keys(test_user2_password)
        self.driver.find_element_by_id("submit").click()

        time.sleep(2)

        assert url_for('home.home_page') in self.driver.current_url

        login_message = self.driver.find_element_by_id("alert").text
        assert "Login Successful. Welcome!" in login_message

    def test_login_invalid_email_format(self):
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("profile_link"))
        hover.perform()
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("user_link"))
        hover.perform()
        element = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.ID, "login_link")))
        element.click()
        time.sleep(1)  

        self.driver.find_element_by_id("email").send_keys("invalid_email")
        self.driver.find_element_by_id("password").send_keys(test_user2_password)
        self.driver.find_element_by_id("submit").click()

        time.sleep(2)

        error_message = self.driver.find_element_by_id("error_email").text
        assert "Invalid email address" in error_message

    def test_login_wrong_email(self):
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("profile_link"))
        hover.perform()
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("user_link"))
        hover.perform()
        element = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.ID, "login_link")))
        element.click()
        time.sleep(1)  

        self.driver.find_element_by_id("email").send_keys(test_user1_email)
        self.driver.find_element_by_id("password").send_keys(test_user2_password)
        self.driver.find_element_by_id("submit").click()

        time.sleep(2)

        error_message = self.driver.find_element_by_id("error_email").text
        assert "Login Unsuccessful. Please check email and password" in error_message

    def test_login_wrong_password(self):
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("profile_link"))
        hover.perform()
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("user_link"))
        hover.perform()
        element = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.ID, "login_link")))
        element.click()
        time.sleep(1)  

        self.driver.find_element_by_id("email").send_keys(test_user2_email)
        self.driver.find_element_by_id("password").send_keys(test_user1_password)
        self.driver.find_element_by_id("submit").click()

        time.sleep(2)

        error_message = self.driver.find_element_by_id("error_email").text
        assert "Login Unsuccessful. Please check email and password" in error_message

if __name__ == '__main__':
    unittest.main()
