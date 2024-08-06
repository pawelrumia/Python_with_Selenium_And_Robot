from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def do_click(self, locator):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(locator)).click()

    def send_keys(self, locator, text):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_text(self, locator):
        return WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(locator)).text

    def is_enabled(self, locator):
        return bool(WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(locator)))

    def get_title(self, title):
        WebDriverWait(self.driver, 3).until(EC.title_is(title))
        return self.driver.title
