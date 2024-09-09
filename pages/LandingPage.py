import allure
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from locators.locators import InternalPages
from pages.CommonMethods import CommonElementMethods


class LandingPage(CommonElementMethods):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Opening heroku training website")
    def open_page(self):
        self.driver.get("https://the-internet.herokuapp.com/")

    @allure.step("Getting title of the page")
    def get_page_title(self):
        return self.driver.title

    def click_add_element_button(self):
        self.driver.find_element(*InternalPages.add_element_button).click()

    def verify_if_checkbox_is_checked(self, checkbox_number):
        checkbox = InternalPages.checkbox1 if checkbox_number == 1 else InternalPages.checkbox2
        (WebDriverWait(self.driver, 5, 2, (NoSuchElementException, StaleElementReferenceException))
         .until(ec.staleness_of(checkbox)))
        yield checkbox.__getattribute__("checked") is not None

    def verify_attribute_of_element_exists(self, xpath, attribute):
        searched_element = self.driver.find_element_by_xpath(xpath)
        return searched_element.get_attribute(attribute) is not None



