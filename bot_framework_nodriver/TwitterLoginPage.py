import nodriver
from nodriver import Element
from selenium.webdriver import Keys

from utils.LoginDataItem import LoginDataItem
from utils.cookies import load_cookies
from .TwitterBasePage import TwitterBasePage


class TwitterLoginPage(TwitterBasePage):
    login_button_locator: str = "//*[contains(@*, '/login')]"

    username_locator: str = "//input[@*='username']"
    password_locator: str = "//input[@*='password']"

    profile_link_locator: str = "//*[@data-testid='AppTabBar_Profile_Link']"
    _page: nodriver.Tab

    @property
    def _login_url(self):
        return f"{self.BASE_URL}/i/flow/login"

    async def open_login_page(self):
        try:
            await self.click_login_button()
        except Exception as e:
            self._page = await self._browser.get(self._login_url)

    async def click_login_button(self):
        # self.wait.until(EC.element_to_be_clickable(self.login_button_locator)).click()
        await self._page.find(self.login_button_locator)

    async def type_username(self, username: str):
        elem: Element = await self._page.find(self.username_locator)
        await elem.send_keys(username)
        await elem.send(Keys.ENTER)

    async def type_password(self, password: str):
        elem: Element = await self.login_page.find(self.password_locator)
        await elem.send_keys(password)
        await elem.send(Keys.ENTER)

    def _login(self, username: str, password: str):
        self.open_twitter()
        self.open_login_page()

        self.type_username(username)
        self.type_password(password)
        self._page.find(self.profile_link_locator)

    def login(self, account: LoginDataItem):
        load_status = self.load_cookies(account)
        if not load_status:
            self._login(account.login, account.password)
            self.save_cookies(account)

