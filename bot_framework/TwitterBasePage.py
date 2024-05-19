import random
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class TwitterBasePage:
    _driver: WebDriver

    BASE_URL: str = "https://x.com"

    def __init__(self, driver: WebDriver):
        self._driver = driver

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @property
    def wait(self) -> WebDriverWait:
        return WebDriverWait(self.driver, 60)

    @property
    def wait_short(self) -> WebDriverWait:
        return WebDriverWait(self.driver, 15)

    def open_twitter(self):
        self._driver.get(self.BASE_URL)

    @staticmethod
    def sleep_in_range(a: int, b: int):
        random_time = (random.randint(a*1000, b*1000) / 1000)
        time.sleep(random_time)

    @staticmethod
    def sleep_by_number(i: int):
        TwitterBasePage.sleep_in_range(i-1, i+1)

    def type_text_by_letters(self, text: str, element: WebElement):
        self.sleep_by_number(1)

        for char in text:
            element.send_keys(char)
            self.sleep_in_range(0, 1)



