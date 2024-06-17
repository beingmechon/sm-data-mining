import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scraper_interface import CommentScraper

class YouTubeCommentScraper(CommentScraper):
    def __init__(self, video_url, driver):
        self.video_url = video_url
        self.driver = driver

    def scrape_comments(self):
        try:
            self.driver.get(self.video_url)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            scroll_attempts = 0

            while True:
                self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(5)
                new_height = self.driver.execute_script("return document.documentElement.scrollHeight")

                if new_height == last_height:
                    scroll_attempts += 1
                    if scroll_attempts > 5:
                        break
                else:
                    scroll_attempts = 0

                last_height = new_height

            comments = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content-text"]'))
            )
            comment_list = [comment.text for comment in comments]
            html_content = self.driver.page_source

            return comment_list, html_content

        finally:
            self.driver.quit()
