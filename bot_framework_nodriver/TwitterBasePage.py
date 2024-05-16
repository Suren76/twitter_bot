import asyncio
import os
from pathlib import Path

import nodriver
# import asyncio
from nodriver import Browser

from utils.LoginDataItem import LoginDataItem


class TwitterBasePage:
    _browser: Browser

    BASE_URL: str = "https://twitter.com"
    _page: nodriver.Tab

    def __init__(self):
        self.start_driver()

    @classmethod
    async def create(cls):
        return cls()

    async def start_driver(self):
        self._browser = await nodriver.start()
        return self


    @property
    def driver(self) -> Browser:
        return self._browser

    async def wait(self, time_to_sleep: int):
        await self._browser.wait(time_to_sleep)

    def open_twitter(self):
        self._page = asyncio.run(self._browser.get(self.BASE_URL))


    def load_cookies(self, account: LoginDataItem, path_to_cookie_dir=None):
        path_to_cookie_dir = Path(
            os.environ.get("PATH_TO_COOKIES_FOLDER")) if path_to_cookie_dir is None else path_to_cookie_dir
        path_to_cookie_file: Path = Path(path_to_cookie_dir) / f"twitter.{account.login}.data"
        self.driver.cookies.load(path_to_cookie_file)
        return True

    def save_cookies(self, account: LoginDataItem, path_to_save_cookies=None):
        path_to_save_cookies = Path(
            os.environ.get("PATH_TO_COOKIES_FOLDER")) if path_to_save_cookies is None else path_to_save_cookies
        path_to_save_cookies_file = Path(path_to_save_cookies) / f"twitter.{account.login}.data"
        self.driver.cookies.save(path_to_save_cookies_file)
        return True

