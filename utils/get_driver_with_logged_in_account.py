import json
import os
import random
import time
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from bot_framework.TwitterLoginPage import TwitterLoginPage
from utils.LoginDataItem import LoginDataItem


def load_accounts_data_on_env(path_to_accounts_file: Path):
    path_to_accounts_file = Path(path_to_accounts_file)
    path_to_cookies_dir = path_to_accounts_file.parent / "cookies"

    accounts_data_list_raw = open(path_to_accounts_file).read().split("\n")
    accounts_data_list = list(filter(None, accounts_data_list_raw))

    login_data_list = LoginDataItem.get_accounts_list_from_raw_accounts_list(accounts_data_list)
    login_data_list = LoginDataItem.get_accounts_list_on_json_format(login_data_list)

    os.environ["ACCOUNTS_DATA"] = json.dumps(login_data_list)
    os.environ["PATH_TO_ACCOUNTS_FILE"] = str(path_to_accounts_file)
    os.environ["PATH_TO_COOKIES_FOLDER"] = str(path_to_cookies_dir)

    if not os.path.exists(path_to_cookies_dir):
        os.mkdir(path_to_cookies_dir)


# todo: maybe need to use class for that {login_data }
def get_random_account_data() -> LoginDataItem:
    login_data_list = json.loads(os.environ["ACCOUNTS_DATA"])

    login_data = LoginDataItem.from_dict(random.choice(login_data_list))
    return login_data


def get_driver_with_logged_in_account(driver: WebDriver) -> TwitterLoginPage:
    driver.delete_all_cookies()
    driver.refresh()

    login_account_data = get_random_account_data()

    login_page = TwitterLoginPage(driver)
    login_page.open_twitter()

    time.sleep(5)

    login_page.login(login_account_data)

    return login_page
