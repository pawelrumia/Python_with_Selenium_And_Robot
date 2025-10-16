import os
import json
import pytest
import allure
from allure_commons.types import AttachmentType
from utils.driver_factory import DriverFactory


# Ścieżka do config.json w katalogu głównym projektu
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


@pytest.fixture(scope="session")
def config():
    """Wczytuje konfigurację testową z pliku config.json."""
    if not os.path.exists(CONFIG_PATH):
        pytest.exit(f"❌ Brak pliku konfiguracyjnego: {CONFIG_PATH}")
    with open(CONFIG_PATH) as f:
        return json.load(f)


@pytest.fixture(scope="class")
def setup(request, config):
    """Tworzy instancję przeglądarki zgodnie z ustawieniami z config.json."""
    driver = DriverFactory.get_driver(config)
    driver.implicitly_wait(config.get("timeout", 10))
    request.cls.driver = driver

    # Dla testów przed błędem — liczba testów, które nie przeszły
    before_failed = request.session.testsfailed

    # Opcjonalne maksymalizowanie okna
    if config.get("browser") == "firefox":
        driver.maximize_window()

    yield

    # Screenshot w razie błędu
    if request.session.testsfailed != before_failed:
        allure.attach(driver.get_screenshot_as_png(),
                      name="Test failed",
                      attachment_type=AttachmentType.PNG)
    driver.quit()
