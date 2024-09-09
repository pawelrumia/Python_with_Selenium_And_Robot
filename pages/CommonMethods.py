from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec

from locators.locators import HomePageLocators


class CommonElementMethods:
    def __init__(self, driver):
        self.driver = driver

    def click_checkbox(self, checkbox_locator):
        (WebDriverWait(self.driver, 5, 2, (NoSuchElementException, StaleElementReferenceException))
         .until(ec.presence_of_element_located(checkbox_locator)).click())

    def click_tab(self, tab_name):
        locators = {
            'checkboxes': HomePageLocators.checkboxes_tab,
            'context_menu': HomePageLocators.context_menu_tab,
            'dropdown': HomePageLocators.dropdown_tab,
            'add_remove_element': HomePageLocators.add_remove_elements_tab, }

        if tab_name not in locators:
            raise ValueError(f"Unknown tab name: {tab_name}")

        (WebDriverWait(self.driver, 5, 2)
         .until(ec.visibility_of_element_located(locators[tab_name])).click())

    def context_click_the_box(self, retries=3):
        attempt = 0
        while attempt < retries:
            try:
                element = self.driver.find_element(By.ID, "hot-spot")
                actions = ActionChains(self.driver)
                actions.context_click(element).perform()
                return
            except StaleElementReferenceException:
                attempt += 1
                print(f"Attempt {attempt} of {retries} failed due to stale element. Retrying...")
                if attempt >= retries:
                    raise

    def switch_to_alert_and_get_text(self):
        WebDriverWait(self.driver, 5).until(ec.alert_is_present())
        alert = self.driver.switch_to.alert
        return alert.text

    def select_value_from_dropdown_by_value(self, dropdown, value):
        select = Select(dropdown)
        select.select_by_value(value)

    def select_value_from_dropdown_by_text(self, dropdown, text):
        WebDriverWait(self.driver, 5).until(ec.element_selection_state_to_be(dropdown, False))
        select = Select(dropdown)
        select.select_by_visible_text(text)
