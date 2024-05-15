from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class TwitterBasePage:
    _driver: WebDriver

    BASE_URL: str = "https://twitter.com"

    def __init__(self, driver: WebDriver):
        self._driver = driver

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @property
    def wait(self) -> WebDriverWait:
        return WebDriverWait(self.driver, 15)

    def open_twitter(self):
        self._driver.get(self.BASE_URL)

