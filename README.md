# YouTube Comment Clustering and Summarization

This project aims to scrape comments from a YouTube video, cluster them based on similarity, and generate summaries for each cluster using NLP models.

## Features

- **YouTube Comment Scraping:** Scrapes comments from a specified YouTube video using Selenium WebDriver.
- **Comment Cleaning and Translation:** Cleans comments by removing timestamps, special characters, and excessive whitespace. Translates non-English comments to English.
- **Comment Clustering:** Utilizes Sentence Transformers to cluster comments based on semantic similarity.
- **Cluster Summarization:** Generates summaries for each comment cluster for easy understanding of whole cluster of comments.

## Project Structure

```
├── config/
│   ├── settings.py              # Configuration settings
│   └── LOGGING_CONFIG_FILE      # Logging configuration
├── data/
│   ├── comments/                # Directory to store scraped comments
│   ├── cluster_summary/         # Directory to store cluster summaries
│   └── clusters/                # Directory to store comment clusters
├── logs/                        # Directory to store log files
├── notebooks                    # Directory to store ipynb notebooks
├── processors/
│   ├── processor_interface.py   # Abstract base class for processors
│   └── comment_processor.py     # Implements CommentProcessor interface
├── scrapers/
│   ├── scraper_interface.py     # Abstract base class for scrapers
│   └── youtube_scraper.py       # Implements YouTubeCommentScraper
├── utils/
│   ├── dependencies.py          # Setup and initialization functions
│   ├── logger.py                # Logging setup
│   └── setup.py                 # Install dependencies
├── main.py                      # Main script to execute the entire process
├── requirements.txt             # Requirement files
└── README.md                    # Project documentation
```

## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/beingmechon/sm-data-mining.git
   cd sm-data-mining
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Setup WebDriver:**
   - Ensure ChromeDriver is installed. You can use `webdriver_manager` for easy installation.

4. **Configuration:**
   - Adjust settings in `config/settings.py` for video URL, logging configurations, etc.

### Prerequisites

### Command-line Arguments

Run `main.py` to initiate the process. You can specify whether to run in headless mode or not by modifying the `--headless` flag. Provide either `--video_url` or `--comments_file` to determine the source of comments:

- `--headless`: Run Chrome WebDriver in headless mode.
- `--video_url <YouTube Video URL>`: Specify the YouTube video URL to scrape comments from.
- `--comments_file <Path to JSON file>`: Path to a JSON file containing pre-existing comments. This skips the YouTube comment scraping step.

Example usage:

```bash
python main.py --headless --video_url "https://www.youtube.com/watch?v=VIDEO_ID"
```

or

```bash
python main.py --headless --comments_file "path/to/comments.json"
```

### Docker Deployment

You can deploy this project using Docker to ensure consistent behavior across different environments.

#### Building the Docker Image

1. Build the Docker image:

   ```bash
   docker build -t comment-summarizer-app .
   ```

2. Run the Docker container:

   ```bash
   docker run --name comment-summarizer -d comment-summarizer-app https://www.youtube.com/watch?v=YOUR_VIDEO_ID

   ```

#### Accessing Logs

To view application logs, use:

```bash
docker logs comment-summarizer
```

#### Managing Docker Containers

- **Stop Container**: `docker stop comment-summarizer`
- **Start Container**: `docker start comment-summarizer`
- **Remove Container**: `docker rm comment-summarizer`
- **Remove Image**: `docker rmi comment-summarizer-app`

## Future Plans

- **Transliteration Support:** Enhance comment processing to handle transliterated comments effectively.
- **Expand Platform Support:** Extend functionality to scrape and process comments from platforms beyond YouTube, such as Facebook, Instagram, and Twitter.

## Dependencies

- `transformers`
- `selenium`
- `langdetect`
- `webdriver-manager`
- `scikit-learn`
- `sentence-transformers`



## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt) file for details.

## Acknowledgments

- Special thanks to contributors and libraries used in this project.
