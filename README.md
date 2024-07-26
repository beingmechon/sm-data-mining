# YouTube Comment Clustering and Summarization

This project aims to scrape comments from a YouTube video, cluster them based on similarity, and generate summaries for each cluster using NLP models.

## Features

- **YouTube Comment Scraping:** Scrapes comments from a specified YouTube video using Selenium WebDriver.
- **Comment Cleaning and Translation:** Cleans comments by removing timestamps, special characters, and excessive whitespace. Translates non-English comments to English.
- **Comment Clustering:** Utilizes Sentence Transformers to cluster comments based on semantic similarity.
- **Cluster Summarization:** Generates summaries for each comment cluster for easy understanding of whole cluster of comments.
