import time
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from bot_framework.TwitterPostPage import TwitterPostPage
from utils.get_driver_with_logged_in_account import get_driver_with_logged_in_random_account
from utils.get_driver_with_proxy import get_driver_with_proxy


def _like_posts_by_urls(driver: WebDriver, posts_urls: list[str], timeout: int):
    post_page = TwitterPostPage(driver)
    for url in posts_urls:
        print(posts_urls.index(url))
        _post = post_page.get_post_by_url(url)
        _post.click_like_button_and_wait()
        time.sleep(timeout)


def _with_driver_like_posts_by_list_of_urls(urls_list: list[str], timeout: int):
    driver = get_driver_with_proxy()
    login_page = get_driver_with_logged_in_random_account(driver)

    _like_posts_by_urls(login_page.driver, urls_list, timeout)
    return "done"


def like_posts_by_url_file(path_to_file: Path | str, like_per_account: int, timeout: int = 3, timeout_to_accounts_change: int = 60):
    path_to_file = Path(path_to_file)
    urls_list_raw = open(path_to_file).read().split("\n")
    urls_list = list(filter(None, urls_list_raw))

    for i in range(round(len(urls_list)/like_per_account)):
        _with_driver_like_posts_by_list_of_urls(urls_list[i*like_per_account: (i+1)*like_per_account], timeout)
        time.sleep(timeout_to_accounts_change)


