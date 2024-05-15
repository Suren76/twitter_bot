from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from bot_framework.TwitterLoginPage import TwitterLoginPage
from like_posts_by_url import like_posts_by_url_file
from like_posts_on_latest import like_post_on_latest_by_text
from utils.get_driver_with_logged_in_account import get_driver_with_logged_in_account, load_accounts_data_on_env
from utils.get_driver_with_proxy import get_driver_with_proxy, load_proxy_data_on_env


...

...


def like_tweets(
        mode: str,
        likes_count: int,
        threads_count: int,
        links_file: str,
        login_data: str,
        proxy_data: str,
        timeout: int,
        timeout_accounts: int,
        path_to_chromedriver: str,
        text_to_search: str,
        headless: bool
):
    if proxy_data:
        load_proxy_data_on_env(Path(proxy_data))
    if login_data:
        load_accounts_data_on_env(Path(login_data))

    driver = get_driver_with_proxy()

    # cookies = json.loads(open("./cookies.json").read())
    #
    # driver.get(login.BASE_URL)
    # for item in cookies:
    #     login.driver.add_cookie(item)

    login_page = get_driver_with_logged_in_account(driver)

    if mode == "link":
        like_posts_by_url_file(login_page.driver, Path(links_file))

    if mode == "latest_posts":
        like_post_on_latest_by_text(login_page.driver, text_to_search, likes_count, timeout)
