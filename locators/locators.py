from selenium.webdriver.common.by import By


class HomePageLocators:
    add_remove_elements_tab = (By.XPATH, "//a[text()='Add/Remove Elements']")
    checkboxes_tab = (By.XPATH, "//a[text()='Checkboxes']")
    context_menu_tab = (By.XPATH, "//a[text()='Context Menu']")
    # Additional tabs on the home page
    ab_testing_tab = (By.LINK_TEXT, "A/B Testing")
    dropdown_tab = (By.LINK_TEXT, "Dropdown")
    form_auth_tab = (By.LINK_TEXT, "Form Authentication")
    multiple_windows_tab = (By.LINK_TEXT, "Multiple Windows")
    inputs_tab = (By.LINK_TEXT, "Inputs")


class InternalPages:
    add_element_button = (By.XPATH, "//button[text()='Add Element']")
    checkboxes_container = (By.ID, "checkboxes")
    checkboxes = (By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")
    context_box = (By.ID, "hot-spot")
    dropdown = (By.ID, "dropdown")
