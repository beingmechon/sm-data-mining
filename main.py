import json
import os 

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from config.settings import VIDEO_URL
from utils.logger import setup_logging
from utils.dependencies import setup_dependencies, init_setup
from scrapers.youtube_scraper import YouTubeCommentScraper
from processors.comment_processor import CommentClusterSummarizer

def main(headless):
    logger = setup_logging()
    init_setup()

    if headless:
        driver = webdriver.Chrome(options=setup_dependencies())
    else:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        # Step 1: Scrape YouTube Comments
        video_id = VIDEO_URL.split("=")[1]
        scraper = YouTubeCommentScraper(VIDEO_URL, driver)
        comments, html_content = scraper.scrape_comments()

        scraper.save_comments_to_json(os.path.join('./data/comments/', f'comments_{video_id}.json'))

        # with open("data\comments\comments_avffSSsVklU.json", "r", encoding="utf8") as f:
        #     comments = json.load(f)
        #     video_id = "avffSSsVklU"

        # print(comments[0])

        # Step 2: Cluster and Summarize Comments
        summarizer = CommentClusterSummarizer()
        comments = summarizer.process_comments(comments)
        similarity_matrix = summarizer.get_similarity_matrix(comments)
        cluster_labels = summarizer.get_cluster_labels(similarity_matrix, threshold=0.7)

        clusters = {}
        for i, label in enumerate(cluster_labels):
            str_label = str(label)
            if str_label not in clusters:
                clusters[str_label] = []
            clusters[str_label].append(comments[i])

        with open(os.path.join('./data/clusters/', f'comment_cluster_{video_id}.json'), 'w', encoding='utf-8') as f:
            json.dump(clusters, f, ensure_ascii=False, indent=4)

        cluster_summaries = summarizer.generate_cluster_summaries(clusters)
        output = {"cluster_summaries": cluster_summaries}

        with open(os.path.join('./data/cluster_summary/', f'comment_cluster_summaries_{video_id}.json'), 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

        logger.info("YouTube comments have been scraped, clustered, and summarized.")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
    finally:
        driver.quit()

if __name__ == '__main__':
    headless = False
    main(headless)
