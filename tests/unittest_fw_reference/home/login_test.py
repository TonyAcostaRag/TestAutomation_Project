import unittest

from pages.home.Login import Login
from pages.welcome.Welcome import Welcome

import time


class LoginTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Login -- Running before only once')

    def setUp(self):
        print('Login -- Running before once every test')

    def test_valid_login_firefox(self):
        print('Login -- Launching firefox browser...')
        login = Login('firefox')
        login.get_url(login.get_driver(), 'https://www.saucedemo.com/v1/')
        login.login('standard_user', 'secret_sauce')
        time.sleep(2)
        welcome = Welcome('', login.get_driver())

        self.assertTrue(welcome.get_label_products().is_displayed(), 'Element was not displayed.')
        welcome.close_driver()

    def test_valid_login_chrome(self):
        print('Login -- Launching chrome browser...')
        login = Login('chrome')
        login.get_url(login.get_driver(), 'https://www.saucedemo.com/v1/')
        login.login('standard_user', 'secret_sauce')
        time.sleep(3)
        welcome = Welcome('', login.get_driver())

        self.assertTrue(welcome.get_label_products().is_displayed(), 'Element was not displayed.')
        welcome.close_driver()

    def tearDown(self):
        print('Login -- Executed after every test')

    @classmethod
    def tearDownClass(cls):
        print('Login -- Running after only once')


if __name__ == '__main__':
    unittest.main(verbosity=2)
