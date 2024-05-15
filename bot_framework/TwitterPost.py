import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TwitterPost:
    _elem: WebElement

    post_like_locator: tuple[By, str] = (By.XPATH, ".//child::article//*[@role='button'][@data-testid='like']")
    post_unlike_locator: tuple[By, str] = (By.XPATH, ".//child::article//*[@role='button'][@data-testid='unlike']")

    post_like_button_locator: tuple[By, str] = (By.XPATH, ".//child::article//*[@role='button'][contains(@data-testid,'like')]")

    post_link_tag_locator: tuple[By, str] = (By.XPATH, ".//time/..")

    def __init__(self, elem: WebElement):
        self._elem = elem
        self.url = self.get_url_of_post()

    def like(self):
        WebDriverWait(self._elem, 3).until(EC.element_to_be_clickable(self.post_like_locator)).click()

    def unlike(self):
        WebDriverWait(self._elem, 3).until(EC.element_to_be_clickable(self.post_like_locator)).click()

    def click_like_button_and_wait(self):
        WebDriverWait(self._elem, 3).until(EC.element_to_be_clickable(self.post_like_button_locator)).click()
        time.sleep(random.randint(2, 7))
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
            time.sleep(3)


