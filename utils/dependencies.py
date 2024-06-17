from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.settings import CHROMEDRIVER_PATH

def setup_dependencies():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.headless = True
    return chrome_options
