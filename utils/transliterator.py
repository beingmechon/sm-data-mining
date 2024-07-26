import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import json
import requests
from collections import deque

from utils import unicode_mapping

class Mapper:
    def __init__(self, charmap):
        self.codepoint_to_english = {}
        self.codepoint_to_category = {}
        self.codepoint_to_char = {}
        self.populate_map(charmap)
        self.categories = {
            'consonants': 'consonants',
            'pulli': 'pulli',
            'dependent_vowels_two_part': 'vowels',
            'dependent_vowels_left': 'vowels',
            'various_signs': 'vowels',
            'independent_vowels': 'vowels',
            'dependent_vowels_right': 'vowels'
        }

    def populate_map(self, charmap):
        for category, codepoints in charmap.items():
            for codepoint, (char, in_english) in codepoints.items():
                self.codepoint_to_char[codepoint] = char
                if isinstance(in_english, tuple):
                    self.codepoint_to_english[codepoint] = in_english[0]
                else:
                    self.codepoint_to_english[codepoint] = in_english
                self.codepoint_to_category[codepoint] = category

    def in_english(self, c):
        return self.codepoint_to_english.get(c, '')

    def char_type(self, c):
        sub_type = self.codepoint_to_category.get(c, '')
        parent_type = self.categories.get(sub_type, '')
        return parent_type, sub_type


class Transliterator:
    def __init__(self, charmap):
        self.mapper = Mapper(charmap)
        # self.transliteration_url = "https://inputtools.google.com/request"
        self.transliteration_url = 'https://www.google.com/inputtools/request'


    def to_tamil(self, english_text):
        params = {
            'text': english_text,
            'itc': 'ta-t-i0-und',
            'num': 13,
            'cp': 0,
            'cs': 0,
            'ie': 'utf-8',
            'oe': 'utf-8'
        }

        try:
            response = requests.get(self.transliteration_url, params=params)
            response.raise_for_status()

            data = response.json()
            # print(data)
            print(data[1][0][1])
            if data[0] == 'SUCCESS':
                return data[1][0][1][0]
            else:
                return ''
        except requests.exceptions.RequestException as e:
            print(f"Error requesting transliteration: {e}")
            return ''


    def to_english(self, text):
        text = self.preprocess(text)
        text = deque(text)
        output = deque()

        while text:
            c = text.popleft()
            in_english = self.mapper.in_english(c)
            parent_type, sub_type = self.mapper.char_type(c)

            if parent_type == 'pulli':
                if output:
                    output.pop()
            elif parent_type == 'vowels' and sub_type != 'independent_vowels':
                if output:
                    output.pop()
                output.extend(deque(in_english))
            else:
                output.extend(deque(in_english))

        return ''.join(output)

    def preprocess(self, text):
        if isinstance(text, bytes):
            return text.decode('utf-8')
        return text

    def transliterate(self, text):
        words = text.split()
        transliterated_words = [self.to_english(w) for w in words]
        return 0, ' '.join(transliterated_words).lower()

if __name__ == "__main__":
    t = Transliterator(unicode_mapping.charmap)

    # text = "Enna panra? saptiya? Amma appa nalla irukangala?"
    # print("Original: ", text)

    # transliterated = t.to_tamil(text)
    # print("Tanglish to Tamil: ",transliterated)

    # engText = t.transliterate(transliterated)[1]
    # print("Back to English: ", engText)

    # engText1 = t.to_english_api(transliterated)
    # print("Back to English via API: ", engText1)

    output_file = "./output.json"
    json_data = "../data/comments.json"

    output_data = []

    with open(json_data, 'r', encoding='utf-8') as f:
        comments = json.load(f)

        for comment in comments:
            transliterated = t.to_tamil(comment)
            engText = t.transliterate(transliterated)[1]

            output_item = {
                "Original": comment,
                "Tanglish to Tamil": transliterated,
                "Back to English": engText
            }

            output_data.append(output_item)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Output saved to {output_file}")


