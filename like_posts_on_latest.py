import time

import tqdm
from selenium.webdriver.remote.webdriver import WebDriver

from bot_framework.TwitterLoginPage import LockedAccountException
from bot_framework.TwitterPost import FailedLikeException, NotAllowedActionsFailedLikeException
from bot_framework.TwitterSearchPage import TwitterSearchPage, SuspendedAccountException
from utils.LoginDataItem import LoginDataItem
from utils.cookies import CookiesException
from utils.get_driver_with_logged_in_account import get_driver_with_logged_in_account, get_account_datas_list, \
    exclude_account_data_from_file_to_banned_accounts_file, exclude_account_data_from_file_to_locked_accounts_file, login_on_not_allowed_actions
from utils.get_driver_with_proxy import get_driver_with_proxy
from multiprocessing import Pool


def like_posts_on_latest_by_count(search_page: TwitterSearchPage, likes_count: int):
    print("start likes on latest")
    if likes_count <= search_page.get_exists_posts_len():
        search_page.like_tweets_and_get_list_count(likes_count)
        return True

    tweets = search_page.like_tweets_and_get_list()
    print("ok")
    if len(tweets) < likes_count:
        print(f"{len(tweets)=}{ likes_count=}")
        search_page.load_new_tweets()
        tweets = tweets + search_page.like_tweets_and_get_list_count(likes_count-len(tweets))

    if len(tweets) == likes_count:
        return True

    # search_page.driver.close()


def _like_post_on_latest_by_text(account: LoginDataItem, text: str, count: int, timeout: int = 3):
    driver = get_driver_with_proxy()

    try:
        login_page = get_driver_with_logged_in_account(driver, account)
    except CookiesException as e:
        driver.quit()

        driver = get_driver_with_proxy()
        login_page = get_driver_with_logged_in_account(driver, account)

    search_page = TwitterSearchPage(login_page.driver)
    # search_page.close_boost_your_privicy()
    search_page.is_account_suspended()

    try:
        search_page.search_by_web(text)
    except Exception as e:
        search_page.search_by_url_on_latest(text)
    search_page.is_app_face_to_rate_limits()

    try:
        res = like_posts_on_latest_by_count(search_page, count)
    except NotAllowedActionsFailedLikeException as e:
        print(f"repeat login {account}")
        login_on_not_allowed_actions(search_page.driver, account)

        # todo: refactoring: clean code and split to funcs
        # search_page = TwitterSearchPage(search_page.driver)
        # search_page.close_boost_your_privicy()
        search_page.is_account_suspended()

        try:
            search_page.search_by_web(text)
        except Exception as e:
            search_page.search_by_url_on_latest(text)
        search_page.is_app_face_to_rate_limits()


        res = like_posts_on_latest_by_count(search_page, count)
    except (FailedLikeException, SuspendedAccountException) as e:
        search_page.close()
        raise e

    search_page.close()
    print(res)
    return res


def like_post_on_latest_by_text(account: LoginDataItem, text: str, count: int, timeout: int = 3, timeout_to_accounts_change: int = 15):
    try:
        _like_post_on_latest_by_text(account, text, count, timeout)
        TwitterSearchPage.sleep_by_number(timeout_to_accounts_change)
    except LockedAccountException as e:
        if type(e) is LockedAccountException:
            print(f"this account is locked: {str(account)}")
        exclude_account_data_from_file_to_locked_accounts_file(account)
    except (FailedLikeException, SuspendedAccountException) as e:
        if type(e) is FailedLikeException:
            print(f"like failed with this account: {str(account)}")
        if type(e) is SuspendedAccountException:
            print(f"this account is suspended: {str(account)}")
        # print(f"like failed with this account: {str(account)}")
        exclude_account_data_from_file_to_banned_accounts_file(account)


def like_posts_on_latest_by_text(text: str, count: int, timeout: int = 3, timeout_to_accounts_change: int = 15, process_count: int = 1):
    accounts_list = get_account_datas_list()
    print("accounts loads")

    if process_count == 1:
        print("start 1 process")
        for account in tqdm.tqdm(accounts_list):
            like_post_on_latest_by_text(account, text, count, timeout, timeout_to_accounts_change)

    def __multiprocess_func(_account: LoginDataItem):
        print("start multiprocess func")
        like_post_on_latest_by_text(_account, text, count, timeout, timeout_to_accounts_change)
        print("end multiprocess func")


    if process_count > 1:
        print(f"start {process_count} process")
        with Pool(process_count) as p:
            p.map(
                __multiprocess_func, accounts_list
            )
