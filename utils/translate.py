import os
import sys
from typing import Dict

import torch

from langdetect import detect, LangDetectException
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from ai4bharat.transliteration import XlitEngine
from IndicTransTokenizer.IndicTransTokenizer import IndicProcessor

from indicLID import IndicLID
from lang_code import LANGUAGE_CODES

# Constants for IndicLID model thresholds
INDICLID_THRESHOLD = 0.6
ROMANLID_THRESHOLD = 0.9

# Initialize IndicLID model
IndicLID_model = IndicLID(input_threshold=INDICLID_THRESHOLD, roman_lid_threshold=ROMANLID_THRESHOLD)

def detect_language(text):
    """ 
    Outputs: 
    if indic 'tam_Taml' or 'tam_Latn'
    if english 'eng_Latn' or 'en'
    if others 'fr' or 'ru' or 'du'
    """

    try:
        # Batch predict with batch size 1
        batch_size = 1
        outputs = IndicLID_model.batch_predict([text], batch_size)
        original_text, detected_lang, confidence, model = outputs[0]

        # Handle cases where IndicLID detects language as "other"
        if detected_lang == "other" or confidence <= 0.8:
            lang = detect(text)
            confidence = -1
            return original_text, lang, confidence, "detect_function"
        
        # Return results
        return original_text, detected_lang, confidence, model

    except LangDetectException:
        # If langdetect library fails, return unknown
        return text, "Unknown", -1, "detect_function"

def indic_translation(text, src_lang, tgt_lang='eng_Latn'):
    # model_name = "ai4bharat/indictrans2-indic-indic-dist-320M"
    model_name = "ai4bharat/indictrans2-indic-en-1B"
    # model_name = "ai4bharat/indictrans2-indic-en-dist-200M"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)

    ip = IndicProcessor(inference=True)
    batch = ip.preprocess_batch(
        text,
        src_lang=src_lang,
        tgt_lang=tgt_lang,
    )

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    # Tokenize the sentences and generate input encodings
    inputs = tokenizer(
        batch,
        truncation=True,
        padding="longest",
        return_tensors="pt",
        return_attention_mask=True,
    ).to(DEVICE)

    # Generate translations using the model
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            use_cache=True,
            min_length=0,
            max_length=256,
            num_beams=10,
            num_return_sequences=1,
        )

    # Decode the generated tokens into text
    with tokenizer.as_target_tokenizer():
        generated_tokens = tokenizer.batch_decode(
            generated_tokens.detach().cpu().tolist(),
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )

    # Postprocess the translations, including entity replacement
    translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)

    for input_sentence, translation in zip(text, translations):
        print(f"{src_lang}: {input_sentence}")
        print(f"{tgt_lang}: {translation}")

    return translations


def indic_transliterate(text, src_lang):
    "src_lang should be 'ta' or 'ml'"
    e = XlitEngine(src_lang, beam_width=10, src_script_type = "latin", model_type="transformer")
    out = e.translit_sentence(text)
    # print(out)

    res = out[src_lang]
    # print(res)
    return res


def other_translations(text, src_lang):
    tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

    # tokenizer.src_lang = "tel_Telu"
    tokenizer.src_lang = src_lang
    tokenizer.tgt_lang = "eng_Latn"

    inputs = tokenizer(text, return_tensors="pt")

    translated_tokens = model.generate(
        **inputs, forced_bos_token_id=tokenizer.lang_code_to_id["eng_Latn"], max_length=30
    )
    
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]


def get_code(input_lang: str, operation: str, lang_type: str, lang_codes: Dict=LANGUAGE_CODES):
    """
    Detected lang could be 'ta' or 'tam_Taml'
    if its transliteration output should be key
    if its translation output should be value that too Latin code eg"tam_Latn"
    """

    indic_langs = lang_codes["indic"]
    other_langs = lang_codes["others"]

    codes = indic_langs if lang_type == "indic" else other_langs

    if operation == "transliterate":
        for key, values in codes.items():
            if input_lang in values:
                return key
    elif operation == "translation":
        pass

    for key, values in lang_codes.items():
        if key == input_lang:
            lang = key
            break
        elif input_lang in values:
            lang = key
            break
        else:
            lang = input_lang

    return lang

def main(text):
    # text = "hey, world"
    original_text, detected_lang, confidence, model = detect_language(text)


    if detected_lang == "en" or detected_lang == "eng_Latn":
        out = text
    elif model == 'detect_function':
        # src_lang should be in this format "tam_Taml" for translation(indic and other)
        src_lang = get_code(detected_lang)
        out = other_translations(text=text)
    elif "Latn" in detected_lang and model != 'detect_function':
        # Here detected_lang will be "tam_Latn"
        src_lang = get_code(detected_lang, "transliterate", "indic")
        translit_text = indic_transliterate(text, src_lang)
        out = indic_translation(translit_text, src_lang)
    elif model != "detct_function":
        # Detected lang will be "tam_Taml"
        out = indic_translation(text, detected_lang)
    else:
        out = "unknown"

    return out

if __name__ == "__main__":
    main()

