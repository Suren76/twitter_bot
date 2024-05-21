import random
import time

from selenium.common import TimeoutException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from bot_framework.TwitterBasePage import TwitterBasePage
from bot_framework.TwitterPost import TwitterPost, FailedLikeException


class SuspendedAccountException(Exception): pass


class TwitterSearchPage(TwitterBasePage):
    LATEST_TAB_PARAM: str = "&f=live"

    tab_bar_search_icon_locator: tuple[By, str] = (By.XPATH, "//*[@*='/explore']")
    reserve_tab_bar_search_icon_locator: tuple[By, str] = (By.XPATH, "//*[@data-testid='AppTabBar_Explore_Link']")

    search_bar_locator: tuple[By, str] = (By.XPATH, "//*[@data-testid='SearchBox_Search_Input']")

    latest_tab_locator: tuple[By, str] = (By.XPATH, f"//*[contains(@*, '{LATEST_TAB_PARAM}')]")

    tweet_block_locator: tuple[By, str] = (By.XPATH, "//div[@data-testid='cellInnerDiv']")

    faced_rate_limits_popup_locator = (By.XPATH, "//*[text()='Sorry, you are rate limited. Please wait a few moments then try again.']")

    reload_button_upper_text_locator = (By.XPATH, "//*[text()='Something went wrong. Try reloading.']")
    reload_button_locator = (By.XPATH, "//*[contains(text(),'Retry')]")

    suspended_account_message_title_locator = (By.XPATH, "//*[text()='Your account is suspended']")

    two_factor_authentication_setup_suggestion_popup_title = (By.XPATH, "//*[text()='Boost your account security']")

    two_factor_authentication_setup_suggestion_popup_close_button = (By.XPATH, "//button[contains(@aria-label,'Close')]")


    @property
    def search_url(self):
        return f"{self.BASE_URL}/search"

    def get_post_elements_list(self) -> list[WebElement]:
        self.wait.until(
            lambda driver: len(driver.find_elements(*self.tweet_block_locator)) > 3
        )
        tweet_elements_list: list[WebElement] = self.driver.find_elements(*self.tweet_block_locator)
        return tweet_elements_list

    def get_exists_posts_len(self):
        return len(self.get_post_elements_list())

    def search_by_url(self, text_to_search: str):
        url = f"{self.search_url}?q={text_to_search}"
        self.driver.get(url)

    def search_by_url_on_latest(self, text_to_search: str):
        self.search_by_url(text_to_search)
        self.driver.get(self.driver.current_url + self.LATEST_TAB_PARAM)

    def search_by_web(self, text_to_search: str):
        self.driver.find_element(*self.tab_bar_search_icon_locator).click()

        elem: WebElement = self.wait.until(EC.element_to_be_clickable(self.search_bar_locator))
        self.type_text_by_letters(text_to_search, elem)
        elem.send_keys(Keys.ENTER)
        self.sleep_by_number(1)

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
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.sleep_by_number(1)

        ActionChains(self.driver)\
            .scroll_by_amount(0, 150)\
            .scroll_by_amount(0, -150)\
            .perform()
        self.sleep_by_number(3)

    # todo: move to TwitterPost
    def is_app_face_to_rate_limits(self):
        # Something went wrong. Try reloading.
        # Sorry, you are rate limited. Please wait a few moments then try again.
        try:
            print(self.wait_short.until(EC.visibility_of_element_located(self.reload_button_upper_text_locator)))
        except TimeoutException as e:
            print(f"{type(e)=}")
            return

        trys = 3
        while trys > 0:
            print(f"{trys=}")
            self.wait.until(EC.element_to_be_clickable(self.reload_button_locator)).click()

            try:
                self.wait_short.until(EC.element_to_be_clickable(self.tweet_block_locator))
                return
            except TimeoutException as e:
                print(f"{type(e)=}")
                print(e)

            print("start time in range(17, 25)")
            self.sleep_in_range(17, 25)
            trys -= 1

        self.close()
        raise FailedLikeException("Like fails")

    def if_two_factor_setup_exists_close(self):
        try:
            self.wait_short.until(EC.visibility_of_element_located(self.two_factor_authentication_setup_suggestion_popup_title))
            self.wait_short.until(EC.element_to_be_clickable(self.two_factor_authentication_setup_suggestion_popup_close_button)).click()
            print("two factor setup popup closed")
        except TimeoutException as e:
            print("if_two_factor_setup_exists_close \n")
            print(f"{type(e)=}")
            return

    # todo: move to TwitterHomePage
    def is_account_suspended(self):
        # self.sleep_by_number(60)

        self.if_two_factor_setup_exists_close()
        # self.driver.refresh()
        try:
            self.wait_short.until(EC.visibility_of_element_located(self.suspended_account_message_title_locator))
            self.close()
            raise SuspendedAccountException
        except TimeoutException as e:
            print(f"{type(e)=}")
            print(e)
            return


