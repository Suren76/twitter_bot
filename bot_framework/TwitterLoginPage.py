from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utils.LoginDataItem import LoginDataItem
from utils.cookies import load_cookies, save_cookies
from .TwitterBasePage import TwitterBasePage


class TwitterLoginPage(TwitterBasePage):
    login_button_locator: tuple[By, str] = (By.XPATH, "//*[contains(@*, '/login')]")

    username_locator: tuple[By, str] = (By.XPATH, "//input[@*='username']")
    password_locator: tuple[By, str] = (By.XPATH, "//input[@*='password']")

    profile_link_locator: tuple[By, str] = (By.XPATH, "//*[@data-testid='AppTabBar_Profile_Link']")

    @property
    def _login_url(self):
        return f"{self.BASE_URL}/i/flow/login"

    def open_login_page(self):
        try:
            self.click_login_button()
        except Exception as e:
            self._driver.get(self._login_url)
        self.sleep_by_number(2)

    def click_login_button(self):
        self.wait.until(EC.element_to_be_clickable(self.login_button_locator)).click()

    def type_username(self, username: str):
        elem: WebElement = self.wait.until(EC.element_to_be_clickable(self.username_locator))
        self.type_text_by_letters(username, elem)
        elem.send_keys(Keys.ENTER)

    def type_password(self, password: str):
        elem: WebElement = self.wait.until(EC.element_to_be_clickable(self.password_locator))
        self.type_text_by_letters(password, elem)
        elem.send_keys(Keys.ENTER)

    def _login(self, username: str, password: str):
        self.open_twitter()
        self.open_login_page()

        self.type_username(username)
        self.type_password(password)
        self.wait.until(EC.element_to_be_clickable(self.profile_link_locator))

    def is_user_logged_in(self):
        try:
            self.wait_short.until(EC.element_to_be_clickable(self.profile_link_locator))
        except TimeoutException as e:
            return False
        return True

    def login(self, account: LoginDataItem):
        login_status = load_cookies(self.driver, account)
        self.driver.refresh()

        if login_status:
            login_status = self.is_user_logged_in()

        if not login_status:
            self._login(account.login, account.password)
        save_cookies(self.driver, account)

