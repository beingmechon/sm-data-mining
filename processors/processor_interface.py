import re
import os, sys

from abc import ABC, abstractmethod
import logging

from langdetect import detect, LangDetectException
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.transliterator import Transliterator
from utils import unicode_mapping

class CommentProcessor():
    def __init__(self):
        self.translate_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

    # @abstractmethod
    # def process_comments(self, comments):
    #     pass

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

    def translate_comments(self, comments) -> list:
        translated_comments = []
        lang_tokenizer_map = {}

        t = Transliterator(unicode_mapping.charmap)                    

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
                        forced_bos_token_id=tokenizer.convert_tokens_to_ids("eng_Latn"),                        max_length=200,
                        num_beams=4,
                        early_stopping=True)
                    
                    text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

                    # Detect language of translated text and transliterate if necessary
                    lang_new = detect(text)
                    print("new", text, lang_new)
                    if lang_new is not None and lang_new != "en":
                        # print("new", lang_new)
                        text = t.to_tamil(comment)
                        langg = detect(text)
                        print("after", text, langg)
                        tok = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", src_lang=langg)
                        inps = tok(text, return_tensors="pt")
                        translated_tok = self.translate_model.generate(
                        **inps,
                        forced_bos_token_id=tok.convert_tokens_to_ids("eng_Latn"), max_length=200,
                        num_beams=4,
                        early_stopping=True)
                        text = tok.batch_decode(translated_tok, skip_special_tokens=True)[0]
                        print(text)


                    translated_text = self.clean_comment(text)

                    translated_comments.append(translated_text)
                else:
                    comment = self.clean_comment(comment)
                    translated_comments.append(comment)

            except Exception as e:
                logging.error(f"Error occurred while translating comment '{comment}': {str(e)}")
                translated_comments.append(comment)

        return translated_comments



if __name__ == "__main__":
    processor = CommentProcessor()
    comments = ["Yar athu spray adikrathu "]#, "Hola amiga!", "こんにちは、ご機嫌ですか？", "Bonjour, comment ça va?"]
    translated_comments = processor.translate_comments(comments)
    for comment, translated_comment in zip(comments, translated_comments):
        print(f"Original: {comment}\nTranslated: {translated_comment}\n")