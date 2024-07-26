from abc import ABC, abstractmethod

class CommentScraper(ABC):
    @abstractmethod
    def scrape_comments(self):
        pass
