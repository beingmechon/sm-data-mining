import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.settings import CHROMEDRIVER_PATH

def setup_dependencies():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.headless = True
    return chrome_options

def init_setup():
    os.makedirs("./logs/", exist_ok=True)
    os.makedirs("./data/comments", exist_ok=True)
    os.makedirs("./data/cluster_summary", exist_ok=True)
    os.makedirs("./data/clusters", exist_ok=True)

