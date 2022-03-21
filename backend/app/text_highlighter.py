import re
from pathlib import Path
from functools import lru_cache
import unidecode

# 336531 French words. From https://github.com/chrplr/openlexicon/blob/master/datasets-info/Liste-de-mots-francais-Gutenberg,
# to which I added some words like 'puisqu'', 'aujourd'hui, quantique' etc.
FRENCH_DICT = Path('./data/dictionnaire.txt')
if not FRENCH_DICT.exists():    # Check in parent directory
    FRENCH_DICT = Path.cwd().parent / FRENCH_DICT

FRENCH_WORDS = set(FRENCH_DICT.read_text().splitlines())


def highlight(text: str, html_tag: str, reg_expr: re.Pattern, should_highlight= (lambda _: True)) -> str:
    """ Adds html tags to text based on the given regular expression and should_highlight function
    Args:
        text (str): Input text
        html_tag (str): Tag to add around the desired text to highlight
        reg_expr (str): Regular 
        should_highlight (function, optional): Function deciding whether to highlight the match
                                            resulting from the regex. Defaults to (lambda _: True).
    Returns:
        str: Text with the parts we wish to highlight inside html tags
    """

    html_tag_start, html_tag_end = f"<{html_tag}>", f"</{html_tag}>"
    offset = 0
    offset_increment = len(html_tag_start) + len(html_tag_end)

    for match in reg_expr.finditer(text):
        start_pos, end_pos = match.start() + offset, match.end() + offset

        if should_highlight(match.group()):
            text = text[:start_pos] + html_tag_start + text[start_pos: end_pos] +  html_tag_end + text[end_pos:]
            offset += offset_increment
    
    return text


def __is_not_french_word(word: str) -> bool:
    """ Cheks if given word is not in the French dictionary """
    # Check if lowercased and ascii'd word is in the dictionary (e.g. 'Sœur' to 'soeur')
    if word.lower() not in FRENCH_WORDS and unidecode.unidecode(word.lower()) not in FRENCH_WORDS:
        # Remove noms propres, but keep acronyms ?
        if (not word[0].isupper() or word.isupper()):
            return True
    return False


def __is_long_sentence(sentence: str, len_treshold: int = 200) -> bool:
    """ Checks if sentence length is above a given threshold """
    return len(sentence) > len_treshold


french_words_regex = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿœ]{3,}")
sentence_regex = re.compile(r".+?[.!?\n]")
quote_regex = re.compile(r"«.+?»")
list_regex = re.compile(r"(?<=\n)- .+?\n")

@lru_cache(maxsize=20)
def highlight_text(text: str) -> str:
    """ Adds html tags to text for: non-french words; long sentences; sentences inside quotation marks, and lists """

    # Highlight non-french words
    text = highlight(text, "hl_notfrench", french_words_regex, should_highlight=__is_not_french_word)
    # Highlight long sentences
    text = highlight(text, "hl_long", sentence_regex, should_highlight=__is_long_sentence)
    # Highlight text inside quotation marks
    text = highlight(text, "hl_quote", quote_regex)
    # Highlight text inside lists
    text = highlight(text, "hl_list", list_regex)

    return text