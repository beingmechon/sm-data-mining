import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


import googleapiclient.discovery

from scraper_interface import CommentScraper
from api_interface import APIFetch

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

    def get_comments(self) -> list[str]:
        return self.comment_list

    def save_comments_to_json(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.comment_list, f, ensure_ascii=False, indent=4)
        print(f"Comments have been saved to {file_path}")


class YoutubeAPI(APIFetch):
    def __init__(self, api_key: str, videoID: str, part: str="snippet", maxResults: int=100, order:str="relevance", textFormat: str="plainText"):
        self.api_key = api_key
        self.videoID = videoID
        self.part = part
        self.maxResults = maxResults
        self.order = order
        self.textFormat = textFormat

    def fetch_from_api(self, page_token=None):
        api_service_name = "youtube"
        api_version = "v3"
        dev_key = self.api_key
        
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = dev_key)
        
        request = youtube.commentThreads().list(
            part=self.part,
            videoId=self.videoID,
            maxResults=self.maxResults,
            order=self.order,
            page_token=page_token)
        
        response = request.execute()

        return response['items']
    
    def fetch_comments_threads(self):
        raw_comments = []
        page_token = None

        while True:
            raw_data = self.fetch_from_api(page_token)
            
            if raw_data is None:
                break
            
            raw_comments.extend(raw_data.get("items", []))
            page_token = raw_data.get("nextPageToken")

            if not page_token:
                break

        return raw_comments
    
    def fetch_comments(self) -> list[str]:
        api_comments = self.fetch_comments_threads()
        self.comments = [comment['snippet']['topLevelComment']['snippet']['textDisplay'] for comment in api_comments]
        return self.comments
    
    def save_comments_to_json(self, file_path):
        # comments, _ = self.scrape_comments()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.comments, f, ensure_ascii=False, indent=4)
        print(f"Comments have been saved to {file_path}")


if __name__ == '__main__':
    video_url = "https://www.youtube.com/watch?v=sceqq4-kQX8"

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    scraper = YouTubeCommentScraper(video_url, driver)
    comments, html_content = scraper.scrape_comments()
    scraper.save_comments_to_json('comments.json')
    driver.quit()