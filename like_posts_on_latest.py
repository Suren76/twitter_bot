from selenium.webdriver.remote.webdriver import WebDriver

from bot_framework.TwitterSearchPage import TwitterSearchPage


def like_posts_on_latest_by_count(search_page: TwitterSearchPage, likes_count: int):
    tweets = search_page.like_tweets_and_get_list()
    print("ok")
    if len(tweets) < likes_count:
        print(f"{len(tweets)=}{ likes_count=}")
        search_page.load_new_tweets()
        tweets = tweets + search_page.like_tweets_and_get_list_count(likes_count-len(tweets))
    if len(tweets) == likes_count:
        return True


def like_post_on_latest_by_text(driver: WebDriver, text: str, count: int, timeout: int = 3):
    search_page = TwitterSearchPage(driver)

    try:
        search_page.search_by_web(text)
    except Exception as e:
        search_page.search_by_url_on_latest(text)

    return like_posts_on_latest_by_count(search_page, count)

