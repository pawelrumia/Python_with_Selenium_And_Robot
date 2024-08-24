import pytest
import json
import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.chrome.options import Options

from utils.driver_factory import DriverFactory

CONFIG_PATH = r"C:\Users\mazurp2\PycharmProjects\Python_with_Selenium_And_Robot\config.json"
DEFAULT_WAIT_TIME = 10
SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]
DEFAULT_URL = "https://the-internet.herokuapp.com/"


@pytest.fixture(scope='session')
def config():
    config_file = open(CONFIG_PATH)
    return json.load(config_file)


@pytest.fixture(scope="session")
def browser_setup(config):
    if "browser" not in config:
        raise Exception('The config file does not contain "browser"')
    elif config["browser"] not in SUPPORTED_BROWSERS:
        raise Exception(f'"{config["browser"]}" is not a supported browser')
    return config["browser"]


@pytest.fixture(scope='session')
def wait_time_setup(config):
    return config['wait_time'] if 'wait_time' in config else DEFAULT_WAIT_TIME


@pytest.fixture(scope='session')
def url_setup(config):
    return config["base_url"] if "base_url" in config else DEFAULT_URL


@pytest.fixture()
def setup(request, config):
    driver = DriverFactory.get_driver(config)
    driver.implicitly_wait(config["timeout"])
    request.cls.driver = driver
    before_failed = request.session.testsfailed
    if config["browser"] == "firefox":
        driver.maximize_window()
    yield
    if request.session.testsfailed != before_failed:
        allure.attach(driver.get_screenshot_as_png(),
                      name="Test failed", attachment_type=AttachmentType.PNG)
    driver.quit()














# @pytest.fixture(scope="module")
# def setup(request):
#     driver = WebDriverSetup.get_driver()
#     options = Options()
#     options.add_argument(r'--profile-directory=C:\Users\mazurp2\AppData\Local\Google\Chrome\User Data\Profile 1')
#     request.cls.driver = driver
#     yield driver
#     driver.quit()
