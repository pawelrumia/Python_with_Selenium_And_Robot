from selenium.webdriver.common.by import By


class HomePageLocators:
    add_remove_elements_tab = (By.XPATH, "//a[text()='Add/Remove Elements']")
    checkboxes_tab = (By.XPATH, "//a[text()='Checkboxes']")
    context_menu_tab = (By.XPATH, "//a[text()='Context Menu']")
    dropdown_tab = (By.XPATH, "//a[text()='Dropdown']")


class InternalPages:
    add_element_button = (By.XPATH, "//button[text()='Add Element']")
    checkbox1 = (By.XPATH, "//input[1][@type=\"checkbox\"]")
    checkbox2 = (By.XPATH, "//input[2][@type=\"checkbox\"]")
    context_box = (By.ID, "hot-spot")
    dropdown = (By.ID, "dropdown")
