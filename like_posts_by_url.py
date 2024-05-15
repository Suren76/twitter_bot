import time
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from bot_framework.TwitterPostPage import TwitterPostPage


def _like_posts_by_url(driver: WebDriver, posts_urls: list[str], timeout: int = 3):
    post_page = TwitterPostPage(driver)
    for url in posts_urls:
        print(posts_urls.index(url))
        _post = post_page.get_post_by_url(url)
        _post.click_like_button_and_wait()
        time.sleep(timeout)


def like_posts_by_url_file(driver: WebDriver, path_to_file: Path | str):
    path_to_file = Path(path_to_file)
    urls_list_raw = open(path_to_file).read().split("\n")
    urls_list = list(filter(None, urls_list_raw))

    _like_posts_by_url(driver, urls_list)
    return "done"
