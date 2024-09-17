from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class Login(BasePage):
    _textbox_username = (By.XPATH, "//input[@id='user-name']")
    _textbox_password = (By.XPATH, "//input[@id='password']")
    _button_signin = (By.XPATH, "//input[@id='login-button']")

    def __init__(self, driver):
        super().__init__(driver)

    def get_textbox_username(self):
        return self.find_element(self._textbox_username)

    def get_textbox_password(self):
        return self.find_element(self._textbox_password)

    def get_button_signin(self):
        return self.find_element(self._button_signin)

    def go_to_page(self):
        url = 'https://www.saucedemo.com/v1/'
        self.get_url(url)

    def login(self, username, password):
        self.get_textbox_username().send_keys(username)
        self.get_textbox_password().send_keys(password)
        self.get_button_signin().click()
