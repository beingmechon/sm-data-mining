from abc import ABC, abstractmethod
import re

class CommentProcessor(ABC):
    @abstractmethod
    def process_comments(self, comments):
        pass

    @staticmethod
    def remove_timestamps(comments):
        timestamp_pattern = r"\b\d{1,3}:\d{2}:\d{2}\b|\b\d{1,2}:\d{2}\b|\b\d{1,2}:\d{1,2}\b"
        
        timestamp_regex = re.compile(timestamp_pattern)
        cleaned_comments = []
        for comment in comments:
            cleaned_comment = re.sub(timestamp_regex, '', comment)
            # print(f"{comment}=>{cleaned_comment}")
            cleaned_comments.append(cleaned_comment)
        return cleaned_comments
    
    @staticmethod
    def translate_comments(comments):
        pass
