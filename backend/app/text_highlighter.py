import re
from pathlib import Path
import unidecode

# 336531 French words. From https://github.com/chrplr/openlexicon/blob/master/datasets-info/Liste-de-mots-francais-Gutenberg,
# to which I added some words like 'puisqu'', 'aujourd'hui, quantique' etc.
FRENCH_DICT = Path('./data/gutenberg_dictionary.txt')
if not FRENCH_DICT.exists():    # Check in parent directory
    FRENCH_DICT = Path.cwd().parent / FRENCH_DICT

FRENCH_WORDS = set(FRENCH_DICT.read_text().splitlines())


def highlight_non_french_words(text: str, html_tag: str):
    html_tag_start, html_tag_end = f"<{html_tag}>", f"</{html_tag}>"
    offset = 0
    offset_increment = len(html_tag_start) + len(html_tag_end)
    french_words_regex = r"[A-Za-zÀ-ÖØ-öø-ÿœ]{3,}"  # Words of at least 3 letters that can have accents

    for match in re.finditer(french_words_regex, text):
        start_pos, end_pos = match.start() + offset, match.end() + offset
        word = match.group()

        # Check if lowercased and ascii'd word is in the dictionary (e.g. 'Sœur' to 'soeur')
        if word.lower() not in FRENCH_WORDS and unidecode.unidecode(word.lower()) not in FRENCH_WORDS:
            # Remove noms propres, but keep acronyms ?
            if (not word[0].isupper() or word.isupper()):
                text = text[:start_pos] + html_tag_start + text[start_pos: end_pos] +  html_tag_end + text[end_pos:]
                offset += offset_increment

    return text


def highlight_long_sentences(text: str, html_tag: str, len_treshold: int = 225):
    html_tag_start, html_tag_end = f"<{html_tag}>", f"</{html_tag}>"
    offset = 0
    offset_increment = len(html_tag_start) + len(html_tag_end)

    for match in re.finditer(r".+?[.!?\n]", text):
        start_pos, end_pos = match.start() + offset, match.end() + offset
        
        # If sentence has a length above 225 characters, highlight it
        if end_pos - start_pos > len_treshold:
            text = text[:start_pos] + html_tag_start + text[start_pos: end_pos] +  html_tag_end + text[end_pos:]
            offset += offset_increment

    return text

def highlight_text_in_quotations(text: str, html_tag: str):
    html_tag_start, html_tag_end = f"<{html_tag}>", f"</{html_tag}>"
    offset = 0
    offset_increment = len(html_tag_start) + len(html_tag_end)

    for match in re.finditer(r"«.+?»", text):
        start_pos, end_pos = match.start() + offset, match.end() + offset

        text = text[:start_pos] + html_tag_start + text[start_pos: end_pos] +  html_tag_end + text[end_pos:]
        offset += offset_increment

    return text

def highlight_text_in_lists(text: str, html_tag: str):
    html_tag_start, html_tag_end = f"<{html_tag}>", f"</{html_tag}>"
    offset = 0
    offset_increment = len(html_tag_start) + len(html_tag_end)

    for match in re.finditer(r"(?<=\n)- .+?\n", text):
        start_pos, end_pos = match.start() + offset, match.end() + offset

        text = text[:start_pos] + html_tag_start + text[start_pos: end_pos] +  html_tag_end + text[end_pos:]
        offset += offset_increment

    return text
    

def highlight_text(text: str) -> str:
    text = highlight_non_french_words(text, html_tag='hl_notfrench')
    text = highlight_long_sentences(text, html_tag='hl_long', len_treshold=225)
    text = highlight_text_in_quotations(text, html_tag='hl_quote')
    text = highlight_text_in_lists(text, html_tag='hl_list')

    return text