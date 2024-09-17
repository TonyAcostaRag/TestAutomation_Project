from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class Home(BasePage):
    _label_products = (By.XPATH, "//div[@class='product_label']")
    
    def __init__(self, driver):
        super().__init__(driver)

    def get_label_products(self):
        return self.find_element(self._label_products).text
