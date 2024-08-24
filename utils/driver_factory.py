from selenium import webdriver
from helpers.listener import WebDriverListener
from extensions.webDriver_extension import WebDriverExtended


class DriverFactory:
    @staticmethod
    def get_driver(config) -> WebDriverExtended:
        if config["browser"] == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("start-maximized")
            if config["headless_mode"] is True:
                options.add_argument("--headless")
            driver = WebDriverExtended(
                webdriver.Chrome(r"C:\Users\mazurp2\PycharmProjects\Python_with_Selenium_And_Robot\chromedriver.exe",
                                 options=options),
                WebDriverListener(), config
            )
            return driver

        raise Exception("Provide valid driver name")
