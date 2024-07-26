import json
import os
import argparse

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
# from config.settings import VIDEO_URL
from utils.logger import setup_logging
from utils.dependencies import setup_dependencies, init_setup
from AggregateData.aggregate_youtube import YouTubeCommentScraper
from processors.cluster_comments import CommentClusterSummarizer

def main(headless, video_url=None, comments_file=None):
    logger = setup_logging()
    init_setup()

    if headless:
        driver = webdriver.Chrome(options=setup_dependencies())
    else:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        if comments_file:
            with open(comments_file, "r", encoding="utf-8") as f:
                comments = json.load(f)
            video_id = os.path.splitext(os.path.basename(comments_file))[0]  # Extract video_id from filename
        else:
            video_id = video_url.split("=")[1]
            scraper = YouTubeCommentScraper(video_url, driver)
            comments, _ = scraper.scrape_comments()

            scraper.save_comments_to_json(os.path.join('./data/comments/', f'comments_{video_id}.json'))

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
    parser = argparse.ArgumentParser(description='YouTube Comment Clustering and Summarization')
    parser.add_argument('--headless', action='store_true', help='Run Chrome WebDriver in headless mode')
    parser.add_argument('--video_url', type=str, help='YouTube video URL to scrape comments from')
    parser.add_argument('--comments_file', type=str, help='Path to a JSON file containing pre-existing comments')

    args = parser.parse_args()
    
    if not (args.video_url or args.comments_file):
        parser.error('Please provide either --video_url or --comments_file')

    main(args.headless, args.video_url, args.comments_file)
