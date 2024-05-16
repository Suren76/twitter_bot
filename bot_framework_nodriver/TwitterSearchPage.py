import time

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from bot_framework.TwitterBasePage import TwitterBasePage
from bot_framework.TwitterPost import TwitterPost


class TwitterSearchPage(TwitterBasePage):
    LATEST_TAB_PARAM: str = "&f=live"

    tab_bar_search_icon_locator: tuple[By, str] = (By.XPATH, "//*[@*='/explore']")
    reserve_tab_bar_search_icon_locator: tuple[By, str] = (By.XPATH, "//*[@data-testid='AppTabBar_Explore_Link']")

    search_bar_locator: tuple[By, str] = (By.XPATH, "//*[@data-testid='SearchBox_Search_Input']")

    latest_tab_locator: tuple[By, str] = (By.XPATH, f"//*[contains(@*, '{LATEST_TAB_PARAM}')]")

    tweet_block_locator: tuple[By, str] = (By.XPATH, "//div[@data-testid='cellInnerDiv']")

    @property
    def search_url(self):
        return f"{self.BASE_URL}/search"

    def get_post_elements_list(self) -> list[WebElement]:
        self.wait.until(
            lambda driver: len(driver.find_elements(*self.tweet_block_locator)) > 3
        )
        tweet_elements_list: list[WebElement] = self.driver.find_elements(*self.tweet_block_locator)
        return tweet_elements_list

    def search_by_url(self, text_to_search: str):
        url = f"{self.search_url}?q={text_to_search}"
        self.driver.get(url)

    def search_by_url_on_latest(self, text_to_search: str):
        self.search_by_url(text_to_search)
        self.driver.get(self.driver.current_url + self.LATEST_TAB_PARAM)

    def search_by_web(self, text_to_search: str):
        self.driver.find_element(*self.tab_bar_search_icon_locator).click()

        elem: WebElement = self.wait.until(EC.element_to_be_clickable(self.search_bar_locator))
        elem.send_keys(text_to_search)
        elem.send_keys(Keys.ENTER)

        self.wait.until(EC.element_to_be_clickable(self.latest_tab_locator)).click()

    def get_tweets_list(self) -> list[TwitterPost]:
        tweet_elements_list: list[WebElement] = self.get_post_elements_list()
        tweets: list[TwitterPost] = TwitterPost.get_tweets_from_list(tweet_elements_list)
        return tweets

    def like_tweets_and_get_list(self) -> list[TwitterPost]:
        tweet_elements_list: list[WebElement] = self.get_post_elements_list()
        tweets: list[TwitterPost] = TwitterPost.like_tweets_from_list(tweet_elements_list)
        return tweets

    # TODO: remove or refactor functionality
    def like_tweets_and_get_list_count(self, count: int) -> list[TwitterPost]:
        tweet_elements_list: list[WebElement] = self.get_post_elements_list()

        tweets = []

        for tweet_element in tweet_elements_list:
            _tweet = TwitterPost(tweet_element)
            _tweet.click_like_button_and_wait()
            tweets.append(_tweet)
            if len(tweets) == count:
                return tweets

        # tweets: list[TwitterPost] = TwitterPost.like_tweets_from_list(tweet_elements_list)
        return tweets

    def load_new_tweets(self):
        self.driver.execute_script("window.scrollTo(0, 0)")
        ActionChains(self.driver)\
            .scroll_by_amount(0, 150)\
            .scroll_by_amount(0, -150)\
            .perform()
        time.sleep(3)

