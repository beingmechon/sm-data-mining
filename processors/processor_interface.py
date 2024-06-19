import re
from abc import ABC, abstractmethod
import logging

from langdetect import detect, LangDetectException
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class CommentProcessor(ABC):
    def __init__(self):
        self.translate_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

    @abstractmethod
    def process_comments(self, comments):
        pass

    @staticmethod
    def clean_comment(comment):
        try:
            # Remove timestamps
            timestamp_pattern = r"\b\d{1,3}:\d{2}:\d{2}\b|\b\d{1,2}:\d{2}\b|\b\d{1,2}:\d{1,2}\b"
            comment = re.sub(timestamp_pattern, '', comment)
            # print("1: ", comment)

            # # Remove special characters except alphanumeric, space, and punctuation
            comment = re.sub(r'[^\w\s.,?!]', '', comment)
            # print("2: ", comment)

            # Remove new lines and excessive whitespace
            comment = re.sub(r'\s+', ' ', comment).strip()
            # print("3: ", comment)

            return comment
        
        except Exception as e:
            logging.error(f"Error occurred while cleaning comment: {str(e)}")
            return comment

    def clean_translate_comments(self, comments):
        translated_comments = []
        lang_tokenizer_map = {}

        for comment in comments:
            try:
                lang = detect(comment)
                print(lang)
            except LangDetectException as e:
                lang = 'en'
                logging.error(f"Language detection error for comment '{comment}': {str(e)}")

            try:
                if lang not in lang_tokenizer_map:
                    lang_tokenizer_map[lang] = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", src_lang=lang)

                tokenizer = lang_tokenizer_map[lang]
                inputs = tokenizer(comment, return_tensors="pt")
                if lang != 'en':
                    translated_tokens = self.translate_model.generate(
                        **inputs,
                        forced_bos_token_id=tokenizer.lang_code_to_id["eng_Latn"],
                        max_length=200,
                        num_beams=4,
                        early_stopping=True
                    )
                    translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
                    # print("translated_text", translated_text)
                    translated_text = self.clean_comment(translated_text)

                    translated_comments.append(translated_text)
                else:
                    comment = self.clean_comment(comment)
                    translated_comments.append(comment)

            except Exception as e:
                logging.error(f"Error occurred while translating comment '{comment}': {str(e)}")
                translated_comments.append(comment)

        return translated_comments
