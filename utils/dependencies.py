import os, sys
import configparser

config_path = os.path.join(os.path.dirname(os.path.dirname((__file__))), 'confs')
sys.path.insert(0, config_path)
print(sys.path)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from confs.settings import CREDENTIALS_FILE, CHROMEDRIVER_PATH

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

def get_api_key():
    parser = configparser.ConfigParser()
    parser.read(CREDENTIALS_FILE)
    return parser["API KEY"]["YOUTUBE_API_KEY"]


if __name__ == "main":
    # chrome_options = setup_dependencies()
    # driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=chrome_options)
    # init_setup()

    api_key = get_api_key()
    print(f"API Key: {api_key}")