from pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    add_remove_elements_tab = (By.XPATH, "//a[text()='Add/Remove Elements']")

    def __init__(self, driver):
        super().__init__(driver)

    def get_homepage_title(self, title):
        return self.get_title(title)

    def click_add_remove_link_button(self):
        self.do_click(self.add_remove_elements_tab)
