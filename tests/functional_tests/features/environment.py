from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FFServ
from selenium.webdriver.chrome.service import Service as ChromeServ
import os


def before_all(context):
    browser = context.config.userdata.get('browser')
    context.driver = _get_browser(browser)
    context.driver.maximize_window()


def after_all(context):
    if context.driver:
        context.driver.quit()


def _get_browser(browser):
    print(os.getcwd())
    browser_dict = {
        'chrome': [webdriver.Chrome, ChromeServ(executable_path='drivers/chromedriver')],
        'firefox': [webdriver.Firefox, FFServ(executable_path='drivers/geckodriver')]
    }
    return browser_dict[browser][0](service=browser_dict[browser][1])
