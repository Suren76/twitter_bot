from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


from bot_framework.TwitterBasePage import TwitterBasePage
from bot_framework.TwitterPost import TwitterPost


class TwitterPostPage(TwitterBasePage):

    def main_tweet_locator(self, tweet_id: int | str) -> tuple[By, str]:
        return By.XPATH, f"//a[contains(@href, '/status/{str(tweet_id)}')]/ancestor::div[@data-testid='cellInnerDiv']"

    def get_post_by_url(self, url: str) -> TwitterPost:
        tweet_id = self.__get_id_of_tweet(url)

        self.driver.get(url)

        elem: WebElement = self.wait.until(EC.element_to_be_clickable(self.main_tweet_locator(tweet_id)))
        tweet: TwitterPost = TwitterPost(elem)
        return tweet

    def __get_id_of_tweet(self, url: str) -> str:
        return url.split("/status/")[1]



