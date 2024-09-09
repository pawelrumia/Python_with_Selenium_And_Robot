import pytest
import allure

from locators.locators import InternalPages
from pages.LandingPage import LandingPage


@pytest.mark.usefixtures("setup")
class TestHomepage:

    @allure.title("Home page - smoke test")
    @allure.description("Check if home page of Demoblaze has correct title")
    def test_homepage_title(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        assert ("The Internet" == homepage.get_page_title())

    @allure.title("Home page - after click")
    @allure.description("dwojeczka")
    def test_homepage_title_after_click(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('add_remove_element')
        homepage.click_add_element_button()
        assert ("Add/Remove Elements" == homepage.get_page_title())

    @allure.title("Checkboxes")
    @allure.description("Checkboxes click check")
    def test_checkbox_then_verify(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('checkboxes')
        assert ("Checkboxes" == homepage.get_page_title())
        homepage.click_checkbox(InternalPages.checkbox1)
        assert LandingPage.verify_if_checkbox_is_checked(self.driver, 1) is True
        assert LandingPage.verify_if_checkbox_is_checked(self.driver, 2) is True

    @allure.title("Context click test")
    @allure.description("Verify context click message")
    def test_context_click_then_verify(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('context_menu')
        homepage.context_click_the_box()
        assert (homepage.switch_to_alert_and_get_text() == "You selected a context menu")

    @allure.title("Select value from dropdown test")
    @allure.description("Select value from dropdown")
    def test_select_dropdown_value_then_verify(self):
        homepage = LandingPage(self.driver)
        homepage.open_page()
        homepage.click_tab('dropdown')
        homepage.select_value_from_dropdown_by_text(InternalPages.dropdown, 'Option 2')
        assert homepage.verify_attribute_of_element_exists("//select[@id='dropdown']/option[@value='2']", "selected")
