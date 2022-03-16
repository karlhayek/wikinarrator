import re
from pathlib import Path
import unidecode

# 336531 French words. From https://github.com/chrplr/openlexicon/blob/master/datasets-info/Liste-de-mots-francais-Gutenberg,
# to which I added some words like 'puisqu'', 'aujourd'hui, quantique' etc.
french_dict = Path('./data/gutenberg_dictionary.txt')
if not french_dict.exists():    # Check in parent directory
    french_dict = Path.cwd().parent / french_dict

FRENCH_WORDS = set(french_dict.read_text().splitlines())


def highlight_non_french_words(text: str, html_tag: str):
    html_tag_start, html_tag_end = f"<{html_tag}>", f"</{html_tag}>"
    
    invalid_words = []

    french_words_regex = r"[A-Za-zÀ-ÖØ-öø-ÿœ]{3,}"  # Words of at least 3 letters that can have accents
    # french_words_regex = r"[a-zA-ZÀ-ÿ]{3,}"
    # french_words_regex = r"[a-zA-ZÀ-ÿ-]{2,}"

    text_words = re.findall(french_words_regex, text)
    for word in text_words:
        # Check if lowercased and ascii'd word is in the dictionary (e.g. 'Sœur' to 'soeur')
        if word.lower() not in FRENCH_WORDS and unidecode.unidecode(word.lower()) not in FRENCH_WORDS:
            invalid_words.append(word)
    
    # Remove noms propres, but keep acronyms ?
    invalid_words = [word for word in invalid_words if (not word[0].isupper() or word.isupper())]
    
    for word in invalid_words:
        text = re.sub(fr"(?<=\W){word}(?=\W)", f"{html_tag_start}{word}{html_tag_end}", text)
        # text = text.replace(word, f"{html_tag_start}{word}{html_tag_end}")
    
    return text


def highlight_long_sentences(text, html_tag: str, char_treshold: int = 25,):
    return text

def highlight_text(text: str) -> str:
    text = highlight_non_french_words(text, html_tag='hl1')

    text = highlight_long_sentences(text, html_tag='hl2', char_treshold=25)

    return text