import random
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class FailedLikeException(Exception): pass
class NotAllowedActionsFailedLikeException(Exception): pass



class TwitterPost:
    _elem: WebElement

    post_like_locator: tuple[By, str] = (By.XPATH, ".//child::article//*[@role='button'][@data-testid='like']")
    post_unlike_locator: tuple[By, str] = (By.XPATH, ".//child::article//*[@role='button'][@data-testid='unlike']")

    post_like_button_locator: tuple[By, str] = (By.XPATH, ".//child::article//*[@role='button'][contains(@data-testid,'like')]")

    post_link_tag_locator: tuple[By, str] = (By.XPATH, ".//time/..")

    banned_account_failed_like_popup_locator = (By.XPATH, "//*[text()='Your account is suspended and is not permitted to perform this action.']")

    not_allowed_actions_account_failed_like_popup_locator = (By.XPATH, "//*[text()='Your account may not be allowed to perform this action. Please refresh the page and try again.']")

    def __init__(self, elem: WebElement):
        self._elem = elem
        self.url = self.get_url_of_post()

    # TODO: move short wait and other general functionality to BaseComponent class
    @property
    def wait(self):
        return WebDriverWait(self._elem, 15)

    @property
    def wait_short(self):
        return WebDriverWait(self._elem, 5)

    @property
    def wait_long(self):
        return WebDriverWait(self._elem, 60)

    @staticmethod
    def sleep_in_range(a: int, b: int):
        random_time = (random.randint(a*1000, b*1000) / 1000)
        print(f"sleep {random_time}s")
        time.sleep(random_time)

    @staticmethod
    def sleep_by_number(i: int):
        TwitterPost.sleep_in_range(i-1, i+1)

    def is_like_fails_by_banned_account(self):
        try:
            print(self.wait_short.until(EC.visibility_of_element_located(self.banned_account_failed_like_popup_locator)))
        except TimeoutException as e:
            return
        raise FailedLikeException("Like fails")

    def is_like_fails_by_not_allowed_actions(self):
        try:
            print(self.wait_short.until(EC.visibility_of_element_located(self.not_allowed_actions_account_failed_like_popup_locator)))
        except TimeoutException as e:
            return
        raise NotAllowedActionsFailedLikeException("Like fails")

    def is_like_fails(self):
        self.is_like_fails_by_banned_account()
        self.is_like_fails_by_not_allowed_actions()

    def like(self):
        self.wait.until(EC.element_to_be_clickable(self.post_like_locator)).click()

    def unlike(self):
        self.wait.until(EC.element_to_be_clickable(self.post_like_locator)).click()

    def click_like_button(self):
        self.wait.until(EC.element_to_be_clickable(self.post_like_button_locator)).click()

    def click_like_button_and_wait(self):
        self.click_like_button()
        self.is_like_fails()

        self.sleep_in_range(2, 7)
        return self

    def get_url_of_post(self):
        link_tag: WebElement = WebDriverWait(self._elem, 3).until(EC.element_to_be_clickable(self.post_link_tag_locator))
        return link_tag.get_attribute("href")

    @staticmethod
    def get_tweets_from_list(list_of_elements: list[WebElement]) -> list['TwitterPost']:
        return [TwitterPost(elem) for elem in list_of_elements]

    # TODO: maybe remove
    @staticmethod
    def like_tweets_from_list(list_of_elements: list[WebElement]) -> list['TwitterPost']:
        return [TwitterPost(elem).click_like_button_and_wait() for elem in list_of_elements]

    # TODO: maybe remove
    @staticmethod
    def like_tweets(list_of_tweets: list['TwitterPost']):
        import time
        for tweet in list_of_tweets:
            tweet.click_like_button_and_wait()
            tweet.sleep_by_number(3)


