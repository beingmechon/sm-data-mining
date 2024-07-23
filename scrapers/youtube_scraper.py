import time
import json

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
        self.comment_list = []

    def scrape_comments(self):
        try:
            self.driver.get(self.video_url)
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            print("last", last_height)
            scroll_attempts = 0

            new_height = 700
            time.sleep(10)
            # print("top 10 sec over")

            while True:
                # print("new", new_height)
                # self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                self.driver.execute_script(f"window.scrollTo(0, {new_height});")

                # print("10 sec start")
                time.sleep(10)
                # print("10 sec end")
                new_height = self.driver.execute_script("return document.documentElement.scrollHeight")

                if new_height == last_height:
                    scroll_attempts += 1
                    if scroll_attempts > 5:
                        break
                else:
                    scroll_attempts = 0

                last_height = new_height

            comments = WebDriverWait(self.driver, 10, 1).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content-text"]'))
            )
            self.comment_list = [comment.text for comment in comments]
            html_content = self.driver.page_source

            return self.comment_list, html_content

        finally:
            self.driver.quit()

    def save_comments_to_json(self, file_path):
        # comments, _ = self.scrape_comments()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.comment_list, f, ensure_ascii=False, indent=4)
        print(f"Comments have been saved to {file_path}")


if __name__ == '__main__':
    video_url = "https://www.youtube.com/watch?v=sceqq4-kQX8"

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    scraper = YouTubeCommentScraper(video_url, driver)
    comments, html_content = scraper.scrape_comments()
    scraper.save_comments_to_json('comments.json')
    driver.quit()