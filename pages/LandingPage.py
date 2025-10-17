import allure
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
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

    @allure.step("Getting page heading text")
    def get_page_heading(self):
        # Prefer headings inside the .example container (used frequently on the-internet pages)
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, ".example h1,.example h2,.example h3")
                or d.find_elements(By.CSS_SELECTOR, "h1,h2,h3")
            )
        except TimeoutException:
            return ""

        # Try container-first, then fallback to any h1-h3
        headings = self.driver.find_elements(By.CSS_SELECTOR, ".example h1,.example h2,.example h3")
        if not headings:
            headings = self.driver.find_elements(By.CSS_SELECTOR, "h1,h2,h3")
        return headings[0].text if headings else ""

    def click_add_element_button(self):
        self.driver.find_element(*InternalPages.add_element_button).click()

    def click_first_checkbox(self):
        # Wait for list of checkboxes to be present and click the first one
        WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(InternalPages.checkboxes))
        checkboxes = self.driver.find_elements(*InternalPages.checkboxes)
        if not checkboxes:
            raise NoSuchElementException("No checkboxes found on the page")
        checkboxes[0].click()

    def click_second_checkbox(self):
        # Wait for list of checkboxes to be present and click the second one
        WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(InternalPages.checkboxes))
        checkboxes = self.driver.find_elements(*InternalPages.checkboxes)
        if len(checkboxes) < 2:
            raise NoSuchElementException("Less than 2 checkboxes found on the page")
        checkboxes[1].click()

    def verify_if_checkbox_is_checked(self, checkbox_number):
        # Return True/False whether the specified checkbox (1-based index) is selected
        WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(InternalPages.checkboxes))
        checkboxes = self.driver.find_elements(*InternalPages.checkboxes)
        idx = checkbox_number - 1
        if idx < 0 or idx >= len(checkboxes):
            raise IndexError(f"Checkbox number {checkbox_number} is out of range. Found {len(checkboxes)} checkboxes")
        return checkboxes[idx].is_selected()

    def set_checkbox_state(self, checkbox_number, should_be_checked=True):
        """Ensure the checkbox (1-based) is in the required state. Returns the final state (True if selected)."""
        WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(InternalPages.checkboxes))
        checkboxes = self.driver.find_elements(*InternalPages.checkboxes)
        idx = checkbox_number - 1
        if idx < 0 or idx >= len(checkboxes):
            raise IndexError(f"Checkbox number {checkbox_number} is out of range. Found {len(checkboxes)} checkboxes")
        current = checkboxes[idx].is_selected()
        if current != should_be_checked:
            checkboxes[idx].click()
        # Re-evaluate after potential click
        return checkboxes[idx].is_selected()

    def click_tab(self, tab_name, wait_for_url_change=True):
        locators = {
            'checkboxes': HomePageLocators.checkboxes_tab,
            'context_menu': HomePageLocators.context_menu_tab,
            'add_remove_element': HomePageLocators.add_remove_elements_tab,
            'ab_testing': HomePageLocators.ab_testing_tab,
            'dropdown': HomePageLocators.dropdown_tab,
            'form_auth': HomePageLocators.form_auth_tab,
            'multiple_windows': HomePageLocators.multiple_windows_tab,
            'inputs': HomePageLocators.inputs_tab,
        }

        if tab_name not in locators:
            raise ValueError(f"Unknown tab name: {tab_name}")

        before = self.driver.current_url
        elem = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(locators[tab_name]))
        elem.click()

        if wait_for_url_change:
            try:
                WebDriverWait(self.driver, 5).until(lambda d: d.current_url != before)
            except TimeoutException:
                # fallback: wait for a heading or .example to be present
                try:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".example,h1,h2,h3")))
                except TimeoutException:
                    pass

    def get_current_url(self):
        return self.driver.current_url

    def context_click_the_box(self, retries=3, accept_alert=True):
        """Context-click the box and optionally wait for and accept the resulting alert, returning its text if any."""
        attempt = 0
        while attempt < retries:
            try:
                element = self.driver.find_element(By.ID, "hot-spot")
                actions: ActionChains = ActionChains(self.driver)
                actions.context_click(element).perform()
                # After performing, wait briefly for an alert and accept it to avoid teardown failures
                if accept_alert:
                    try:
                        WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                        alert = self.driver.switch_to.alert
                        text = alert.text
                        try:
                            alert.accept()
                        except Exception:
                            pass
                        return text
                    except TimeoutException:
                        return None
                return None
            except StaleElementReferenceException:
                attempt += 1
                print(f"Attempt {attempt} of {retries} failed due to stale element. Retrying...")
                if attempt >= retries:
                    raise

    def switch_to_alert_and_get_text(self):
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        text = alert.text
        # Accept the alert so it doesn't remain open and interfere with teardown
        try:
            alert.accept()
        except Exception:
            pass
        return text
