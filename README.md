# YouTube Comment Clustering and Summarization

This project aims to scrape comments from a YouTube video, cluster them based on similarity, and generate summaries for each cluster using NLP models.

## Features

- **YouTube Comment Scraping:** Scrapes comments from a specified YouTube video using Selenium WebDriver.
- **Comment Cleaning and Translation:** Cleans comments by removing timestamps, special characters, and excessive whitespace. Translates non-English comments to English.
- **Comment Clustering:** Utilizes Sentence Transformers to cluster comments based on semantic similarity.
- **Cluster Summarization:** Generates summaries for each comment cluster using the BART model for conditional text generation.

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

## Usage

Run `main.py` to initiate the process. You can specify whether to run in headless mode or not by modifying the `headless` flag in `main.py`.

```bash
python main.py
```

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
