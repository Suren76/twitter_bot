import json
import os
from pathlib import Path

from selenium.common import InvalidCookieDomainException, UnableToSetCookieException, NoSuchCookieException
from selenium.webdriver.remote.webdriver import WebDriver

from utils.LoginDataItem import LoginDataItem


class CookiesException(Exception): pass


def load_cookies(driver: WebDriver, account: LoginDataItem, path_to_cookie_dir: Path | str = None):
    path_to_cookie_dir = Path(os.environ.get("PATH_TO_COOKIES_FOLDER")) if path_to_cookie_dir is None else path_to_cookie_dir
    path_to_cookie_file: Path = Path(path_to_cookie_dir) / f"{account.login}.json"

    cookies = []

    try:
        if os.path.exists(path_to_cookie_file):
            cookies = json.loads(open(path_to_cookie_file, "r+").read())
        else:
            return False
    except FileNotFoundError as e:
        print(f"{type(e)=}")
        print(e)
        return False

    if len(cookies) == 0: return False

    # login.driver.get(login.BASE_URL)

    try:
        for item in cookies:
            driver.add_cookie(item)
    except (InvalidCookieDomainException, UnableToSetCookieException, NoSuchCookieException) as e:
        print(f"{type(e)=}")
        print(e)

        os.remove(path_to_cookie_file)
        raise CookiesException
        # return False

    return True


def save_cookies(driver: WebDriver, account: LoginDataItem, path_to_save_cookies: Path | str = None):
    path_to_save_cookies = Path(os.environ.get("PATH_TO_COOKIES_FOLDER")) if path_to_save_cookies is None else path_to_save_cookies
    path_to_save_cookies_file = Path(path_to_save_cookies) / f"{account.login}.json"

    open(path_to_save_cookies_file, "w+").write(json.dumps(driver.get_cookies()))

