from abc import ABC, abstractmethod

class CommentProcessor(ABC):
    @abstractmethod
    def process_comments(self, comments):
        pass
