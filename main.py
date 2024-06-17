# main.py
import time
import json
from selenium import webdriver
from config.settings import VIDEO_URL
from utils.logger import setup_logging
from utils.dependencies import setup_dependencies
from scrapers.youtube_scraper import YouTubeCommentScraper
from processors.comment_processor import CommentClusterSummarizer

def main():
    # Setup
    logger = setup_logging()
    driver = webdriver.Chrome(options=setup_dependencies())

    try:
        # Step 1: Scrape YouTube Comments
        scraper = YouTubeCommentScraper(VIDEO_URL, driver)
        comments, html_content = scraper.scrape_comments()

        # Save comments and HTML content
        scraper.save_comments_to_json(comments, html_content)

        # Step 2: Cluster and Summarize Comments
        summarizer = CommentClusterSummarizer()
        similarity_matrix = summarizer.get_similarity_matrix(comments)
        cluster_labels = summarizer.get_cluster_labels(similarity_matrix, threshold=0.7)

        clusters = {}
        for i, label in enumerate(cluster_labels):
            str_label = str(label)
            if str_label not in clusters:
                clusters[str_label] = []
            clusters[str_label].append(comments[i])

        with open('comment_cluster.json', 'w', encoding='utf-8') as f:
            json.dump(clusters, f, ensure_ascii=False, indent=4)

        cluster_summaries = summarizer.generate_cluster_summaries(clusters)
        output = {"cluster_summaries": cluster_summaries}

        with open('comment_cluster_summaries.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

        logger.info("YouTube comments have been scraped, clustered, and summarized.")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()