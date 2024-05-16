import time

from selenium.webdriver.remote.webdriver import WebDriver

from bot_framework.TwitterSearchPage import TwitterSearchPage
from utils.LoginDataItem import LoginDataItem
from utils.get_driver_with_logged_in_account import get_driver_with_logged_in_account, get_account_datas_list
from utils.get_driver_with_proxy import get_driver_with_proxy


def like_posts_on_latest_by_count(search_page: TwitterSearchPage, likes_count: int):
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


def _like_post_on_latest_by_text(account: LoginDataItem, text: str, count: int, timeout: int = 3):
    driver = get_driver_with_proxy()
    login_page = get_driver_with_logged_in_account(driver, account)

    search_page = TwitterSearchPage(login_page.driver)

    try:
        search_page.search_by_web(text)
    except Exception as e:
        search_page.search_by_url_on_latest(text)

    return like_posts_on_latest_by_count(search_page, count)


def like_post_on_latest_by_text(text: str, count: int, timeout: int = 3, timeout_to_accounts_change: int = 15):
    accounts_list = get_account_datas_list()

    for account in accounts_list:
        _like_post_on_latest_by_text(account, text, count, timeout)
        time.sleep(timeout_to_accounts_change)

