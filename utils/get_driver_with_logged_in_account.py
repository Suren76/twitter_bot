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


def get_account_datas_list() -> list[LoginDataItem]:
    login_data_list = json.loads(os.environ["ACCOUNTS_DATA"])
    login_data = LoginDataItem.get_accounts_list_from_dict_accounts_list(login_data_list)
    return login_data


# todo: maybe need to use class for that {login_data }
def get_random_account_data() -> LoginDataItem:
    return random.choice(get_account_datas_list())


def get_driver_with_logged_in_account(driver: WebDriver, login_data_item: LoginDataItem) -> TwitterLoginPage:
    driver.delete_all_cookies()
    driver.refresh()

    login_page = TwitterLoginPage(driver)
    login_page.open_twitter()

    time.sleep(5)

    login_page.login(login_data_item)

    return login_page


def get_driver_with_logged_in_random_account(driver: WebDriver):
    login_account_data = get_random_account_data()
    return get_driver_with_logged_in_account(driver, login_account_data)

