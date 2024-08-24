import allure
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import HomePageLocators, InternalPages


class LandingPage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Opening heroku training website")
    def open_page(self):
        self.driver.get("https://the-internet.herokuapp.com/")

    @allure.step("Getting title of the page")
    def get_page_title(self):
        return self.driver.title

    def click_add_element_button(self):
        self.driver.find_element(*InternalPages.add_element_button).click()

    def click_first_checkbox(self):
        (WebDriverWait(self.driver, 5, 2, (NoSuchElementException, StaleElementReferenceException))
         .until(EC.presence_of_element_located(*InternalPages.checkbox1)).click())

    def click_second_checkbox(self):
        (WebDriverWait(self.driver, 5, 2, (NoSuchElementException, StaleElementReferenceException))
         .until(EC.presence_of_element_located(*InternalPages.checkbox2)).click())

    def verify_if_checkbox_is_checked(self, checkbox_number):
        checkbox = InternalPages.checkbox1 if checkbox_number == 1 else InternalPages.checkbox2
        (WebDriverWait(self.driver, 5, 2, (NoSuchElementException, StaleElementReferenceException))
         .until(EC.staleness_of(checkbox)))
        yield checkbox.__getattribute__("checked") is not None

    def click_tab(self, tab_name):
        locators = {
            'checkboxes': HomePageLocators.checkboxes_tab,
            'context_menu': HomePageLocators.context_menu_tab,
            'add_remove_element': HomePageLocators.add_remove_elements_tab, }

        if tab_name not in locators:
            raise ValueError(f"Unknown tab name: {tab_name}")

        (WebDriverWait(self.driver, 5, 2)
         .until(EC.visibility_of_element_located(locators[tab_name])).click())

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
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        return alert.text
