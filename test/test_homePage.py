import pytest
import allure

from locators.locators import InternalPages
from pages.LandingPage import LandingPage
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import InternalPages, HomePageLocators

@pytest.mark.usefixtures("setup")
class TestHomepage:
    # annotate driver to satisfy static analyzers (fixture assigns request.cls.driver at runtime)
    driver: WebDriver | None = None

    @allure.feature("Home page")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Home page - smoke test")
    @allure.description("Check if home page of The Internet has correct title and heading visibility")
    def test_homepage_title(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1,h2,h3,.example h1,.example h2,.example h3")))
        heading = homepage.get_page_heading()
        assert homepage.get_page_title() == "The Internet", "❌ Page title is incorrect"
        assert heading and len(heading) > 0, "❌ Page heading is missing or empty"

    @allure.feature("Home page")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Home page - after click")
    def test_homepage_title_after_click(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('add_remove_element')
        homepage.click_add_element_button()
        delete_btn_locator = (By.XPATH, "//button[text()='Delete']")
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(delete_btn_locator))
        delete_btn = self.driver.find_element(*delete_btn_locator)
        assert delete_btn.is_displayed(), "Delete button should be visible after adding element"
        assert ("The Internet" == homepage.get_page_title())
        assert ("Add/Remove Elements" == homepage.get_page_heading())

    @allure.feature("Checkboxes")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Checkboxes")
    @allure.description("Checkboxes click check")
    def test_checkbox_then_verify(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('checkboxes')
        # Wait for container
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(InternalPages.checkboxes_container))
        checkboxes = self.driver.find_elements(*InternalPages.checkboxes)
        assert len(checkboxes) >= 2, "At least two checkboxes expected"
        assert all(cb.is_displayed() for cb in checkboxes[:2]), "Checkboxes should be displayed"
        assert all(cb.is_enabled() for cb in checkboxes[:2]), "Checkboxes should be enabled"
        homepage.set_checkbox_state(1, True)
        homepage.set_checkbox_state(2, True)
        assert homepage.verify_if_checkbox_is_checked(1) is True
        assert homepage.verify_if_checkbox_is_checked(2) is True

    @allure.feature("A/B Testing")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("A/B Testing tab")
    def test_ab_testing_tab(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('ab_testing')
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".example p")))
        assert '/abtest' in homepage.get_current_url()
        assert 'test' in homepage.get_page_heading().lower()
        para = self.driver.find_element(By.CSS_SELECTOR, ".example p")
        assert para.is_displayed(), "A/B Testing paragraph should be visible"

    @allure.feature("Dropdown")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Dropdown tab")
    def test_dropdown_tab(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('dropdown')
        select_locator = (By.ID, 'dropdown')
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(select_locator))
        select_elem = self.driver.find_element(*select_locator)
        assert select_elem.is_displayed(), "Dropdown should be visible"
        options = select_elem.find_elements(By.TAG_NAME, 'option')
        assert len(options) >= 1, "Dropdown should have at least one option"

    @allure.feature("Authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Form Authentication tab and invalid login warning")
    def test_form_auth_tab(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('form_auth')
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'username')))
        user = self.driver.find_element(By.ID, 'username')
        pwd = self.driver.find_element(By.ID, 'password')
        submit = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert user.is_displayed() and pwd.is_displayed() and submit.is_displayed(), "Login elements should be visible"
        user.clear(); user.send_keys('invalid')
        pwd.clear(); pwd.send_keys('invalid')
        submit.click()
        flash_locator = (By.ID, 'flash')
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(flash_locator))
        flash = self.driver.find_element(*flash_locator)
        txt = flash.text.lower()
        assert 'your username is invalid' in txt or 'invalid' in txt, f"Expected invalid login warning, got: {txt}"

    @allure.feature("Windows")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Multiple Windows tab")
    def test_multiple_windows_tab(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('multiple_windows')
        link_locator = (By.LINK_TEXT, 'Click Here')
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(link_locator)).click()
        handles = self.driver.window_handles
        assert len(handles) >= 2, "A new window should open"
        self.driver.switch_to.window(handles[-1])
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'h3')))
        assert 'new window' in homepage.get_page_heading().lower()
        self.driver.close()
        self.driver.switch_to.window(handles[0])

    @allure.feature("Inputs")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Inputs tab")
    def test_inputs_tab(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('inputs')
        input_locator = (By.CSS_SELECTOR, 'input[type="number"], input[type="text"], input')
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(input_locator))
        inp = self.driver.find_element(By.TAG_NAME, 'input')
        assert inp.is_displayed()
        inp.clear(); inp.send_keys('42')
        assert inp.get_attribute('value') == '42'

    @allure.feature("Context menu")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Context click test")
    @allure.description("Verify context click message and visibility of target box")
    def test_context_click_then_verify(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('context_menu')
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'hot-spot')))
        box = self.driver.find_element(By.ID, 'hot-spot')
        assert box.is_displayed(), "Context menu target box should be visible"
        alert_text = homepage.context_click_the_box()
        assert (alert_text == "You selected a context menu")


    @allure.title("Select value from dropdown test")
    @allure.description("Select value from dropdown")
    def test_select_dropdown_value_then_verify(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('dropdown')
        homepage.select_value_from_dropdown_by_text(InternalPages.dropdown, 'Option 2')
        assert homepage.verify_attribute_of_element_exists("//select[@id='dropdown']/option[@value='2']", "selected")

