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

    path_to_account_files_json = path_to_accounts_file.with_suffix(".json")
    open(path_to_account_files_json, "w+").write(json.dumps(login_data_list))

    os.environ["ACCOUNTS_DATA_FILE_JSON"] = str(path_to_account_files_json)

    os.environ["PATH_TO_ACCOUNTS_FILE"] = str(path_to_accounts_file)
    os.environ["PATH_TO_COOKIES_FOLDER"] = str(path_to_cookies_dir)

    if not os.path.exists(path_to_cookies_dir):
        os.mkdir(path_to_cookies_dir)


def get_account_datas_list() -> list[LoginDataItem]:
    login_data_list = json.loads(open(os.environ["ACCOUNTS_DATA_FILE_JSON"]).read())
    login_data = LoginDataItem.get_accounts_list_from_dict_accounts_list(login_data_list)
    return login_data


# todo: maybe need to use class for that {login_data }
def get_random_account_data() -> LoginDataItem:
    return random.choice(get_account_datas_list())


def exclude_account_data_from_file(to_exclude_account_data: LoginDataItem):
    _path_to_accounts_file = Path(os.environ["PATH_TO_ACCOUNTS_FILE"])
    _path_to_excluded_accounts_file = _path_to_accounts_file.with_stem(_path_to_accounts_file.stem + "_excluded")

    excluded_accounts: list[LoginDataItem] = []

    load_accounts_data_on_env(_path_to_accounts_file)

    file_of_account_datas = open(_path_to_accounts_file, "w+")

    if _path_to_excluded_accounts_file.exists():
        excluded_accounts_raw = open(_path_to_excluded_accounts_file).read().split("\n")
        print(f"{excluded_accounts_raw=}")
        excluded_accounts = LoginDataItem.get_accounts_list_from_raw_accounts_list(list(filter(None, excluded_accounts_raw)))
        excluded_accounts.append(to_exclude_account_data)


    # file_of_account_datas.seek(0)
    # file_of_excluded_account_datas.seek(0)

    accounts_list = get_account_datas_list()
    accounts_list_with_excluded_account = list(filter(lambda account: account != to_exclude_account_data, accounts_list))
    print(f"{to_exclude_account_data=} \n")
    print(f"{accounts_list=} \n")
    print(f"{len(accounts_list)=}")
    print(f"{accounts_list_with_excluded_account} \n")
    print(f"{len(accounts_list_with_excluded_account)=}")

    raw_accounts_list_excluded = LoginDataItem.get_accounts_list_on_raw_format(accounts_list_with_excluded_account)
    print(raw_accounts_list_excluded)
    file_of_account_datas.write(raw_accounts_list_excluded)
    file_of_account_datas.close()

    raw_excluded_accounts_list = LoginDataItem.get_accounts_list_on_raw_format(excluded_accounts)
    print(f"{len(excluded_accounts)=}")
    print(f"{len(raw_excluded_accounts_list)=}")
    open(_path_to_excluded_accounts_file, "w+").write(raw_excluded_accounts_list)


def get_driver_with_logged_in_account(driver: WebDriver, login_data_item: LoginDataItem) -> TwitterLoginPage:
    driver.delete_all_cookies()
    driver.refresh()

    login_page = TwitterLoginPage(driver)
    login_page.open_twitter()

    login_page.sleep_by_number(5)

    login_page.login(login_data_item)

    return login_page


def get_driver_with_logged_in_random_account(driver: WebDriver):
    login_account_data = get_random_account_data()
    return get_driver_with_logged_in_account(driver, login_account_data)

