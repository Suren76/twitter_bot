import time
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from bot_framework.TwitterLoginPage import LockedAccountException
from bot_framework.TwitterPost import FailedLikeException
from bot_framework.TwitterPostPage import TwitterPostPage
from bot_framework.TwitterSearchPage import TwitterSearchPage, SuspendedAccountException
from utils.LoginDataItem import LoginDataItem
from utils.cookies import CookiesException
from utils.get_driver_with_logged_in_account import  \
    get_driver_with_logged_in_account, get_account_datas_list, \
    exclude_account_data_from_file_to_locked_accounts_file, exclude_account_data_from_file_to_banned_accounts_file
from utils.get_driver_with_proxy import get_driver_with_proxy


def _like_posts_by_urls(driver: WebDriver, posts_urls: list[str], timeout: int):
    post_page = TwitterPostPage(driver)
    for url in posts_urls:
        print(posts_urls.index(url))
        _post = post_page.get_post_by_url(url)

        search_page = TwitterSearchPage(post_page.driver)
        search_page.is_account_suspended()
        search_page.is_app_face_to_rate_limits()

        _post.click_like_button_and_wait()
        post_page.sleep_by_number(timeout)


def _with_driver_like_posts_by_list_of_urls(urls_list: list[str], account: LoginDataItem, timeout: int):
    driver = get_driver_with_proxy()
    try:
        login_page = get_driver_with_logged_in_account(driver, account)
    except CookiesException as e:
        driver.quit()

        driver = get_driver_with_proxy()
        login_page = get_driver_with_logged_in_account(driver, account)

    _like_posts_by_urls(login_page.driver, urls_list, timeout)
    return "done"


def like_posts_by_url_file(path_to_file: Path | str, like_per_account: int, timeout: int = 3, timeout_to_accounts_change: int = 60):
    accounts_list = get_account_datas_list()

    path_to_file = Path(path_to_file)
    urls_list_raw = open(path_to_file).read().split("\n")
    urls_list = list(filter(None, urls_list_raw))

    for i in range(round(len(urls_list)/like_per_account)):
        try:
            _with_driver_like_posts_by_list_of_urls(urls_list[i*like_per_account: (i+1)*like_per_account], accounts_list[i], timeout)
            TwitterPostPage.sleep_by_number(timeout_to_accounts_change)
        except LockedAccountException as e:
            if type(e) is LockedAccountException:
                print(f"this account is locked: {str(accounts_list[i])}")
            exclude_account_data_from_file_to_locked_accounts_file(accounts_list[i])
        except (FailedLikeException, SuspendedAccountException) as e:
            if type(e) is FailedLikeException:
                print(f"like failed with this account: {str(accounts_list[i])}")
            if type(e) is SuspendedAccountException:
                print(f"this account is suspended: {str(accounts_list[i])}")
            # print(f"like failed with this account: {str(account)}")
            exclude_account_data_from_file_to_banned_accounts_file(accounts_list[i])




