import re
import urllib
from bs4 import BeautifulSoup


def get_first_keyword_position(text: str, keywords: [str], after_keyword=False) -> int:
    """ Gets position of the first found keyword in a text from a list of keywords
    Arguments:
        text {str} -- Text where search should be done
        keywords {[str]} -- List of keywords to search
        after_keyword {bool} -- Whether to return the position after or before the keyword (default: {False})
    Returns:
        int -- Position of the first found keyword in the text. Returns -1 if no keyword was found
    """
    keyword_positions = [(keyword_pos, keyword) for keyword in keywords if (
        keyword_pos := text.find(keyword)) > -1]

    if len(keyword_positions) == 0:
        return -1

    min_keyword_pos, min_keyword = min(keyword_positions)

    return min_keyword_pos + len(min_keyword) if after_keyword else min_keyword_pos


def replace_bullet_points(input_text: str):
    """ Replaces bullet points ('\n* [text]') in text with numbers ('1. ', etc.) """

    new_text = ""
    bullet_point_number = 1
    last_pos = 0
    
    for m in re.finditer(r"(?<=(\n\*)) .+", input_text):
        replace_string = f"{bullet_point_number}." +  m.group()
        new_text += input_text[last_pos:m.start()-1] + replace_string
        
        last_pos = m.end()
        bullet_point_number += 1

    new_text += input_text[last_pos:]

    return new_text


def clean_text(text: str) -> str:
    cleaned_text = text

    # Replace bullet points/lists with numbers 
    # cleaned_text = replace_bullet_points(cleaned_text)

    # Remove items. Remove all text between brackets ? 
    remove_list = [
        " (en)", "(en) ", "(en)", "[Lequel ?]", "[Lesquel ?]", "[Quoi ?],", "[pas clair]", "[Qui ?]"
    ]
    remove_list_regex = [
        # strings starting with "[ref. ]" or "[source ]""
        r"\[réf\..+\]", r"\[source.+\]"
    ]
    for item_to_remove in remove_list:
        cleaned_text = cleaned_text.replace(item_to_remove, "")
    for regex in remove_list_regex:
        cleaned_text = re.sub(regex, "", cleaned_text)


    # Remove text at the end of the article (annexes, bibliographies etc.)
    end_sections_to_stop_at = [
        '== Annexes ==', '== Bibliographie ==', '== Notes et références ==', '== Voir aussi ==',
        '== Œuvres ==', '== Publications ==' ##
    ]

    end_pos = get_first_keyword_position(cleaned_text, end_sections_to_stop_at)
    if end_pos != -1:
        cleaned_text = cleaned_text[:end_pos]

    return cleaned_text


def prepare_text_for_TTS(text: str) -> str:
    """ Prepare text for TTS, removing / replacing characters that are mispronounced by TTS """
    # Replace abbreviations
    abbreviations_list = {
        "av. J.-C": "avant Jésus Christ",
    }
    for to_replace, replacer in abbreviations_list.items():
        text = text.replace(to_replace, replacer)

    replace_list = {
        " (": ", ",                     # Replace parentheses with comas
        ") ": ", ",
    }
    replace_list_regex = {
        r"Mc(?=[A-Z][a-z]+)": "Mac",    # McGellan -> MacGellan
        r"(?!\d+)\/(?=\d+)":  " sur ",  # nombres séparés par '/'
    }
    for to_replace, replacer in replace_list.items():
        text = text.replace(to_replace, replacer)
    for regex_to_replace, replacer in replace_list_regex.items():
        text = re.sub(regex_to_replace, replacer, text)
    
    return text



def extract_title_from_url(url: str) -> str:
    """ Extracts wikipedia article title from a URL. Example: "https://fr.wikipedia.org/wiki/Hedy_Lamarr" returns "Hedy_Lamarr" """
    # Extract title from the URL using a regex
    # ex: from "https://fr.wikipedia.org/wiki/Grandes_d%C3%A9couvertes#Contexte" we get "Grandes_d%C3%A9couvertes#Contexte"
    regex = r"(?<=https:\/\/\S\S\.wikipedia\.org\/wiki.)\S+[^#]$"

    matches = re.findall(regex, url)
    if len(matches) == 0:
        # raise Exception("URL is invalid ! Make sure it is a valid wikipedia article URL")
        return ""
    
    # Sanitize title extracted from the URL
    title = urllib.parse.unquote(matches[0], encoding='utf-8', errors='replace')

    # Remove possible '#' suffix to the URl (ex: from a wiki section)
    title = title.split('#')[0]

    return title


def edit_and_convert_html_text(html_text: str) -> str:
    # These tags should be new lines. These tags are usually used in citations and sometimes in lists
    html_text = html_text.replace("</dd></dl></dd></dl>", "\n</dd></dl></dd></dl>\n")

    soup = BeautifulSoup(html_text, 'html.parser')

    # Add "="'s in headers
    for h2 in soup.find_all("h2"):
        h2.insert_before("\n== ")
        h2.insert_after(" ==\n")

    for h3 in soup.find_all("h3"):
        h3.insert_before("\n=== ")
        h3.insert_after(" ===\n")

    for h4 in soup.find_all("h4"):
        h4.insert_before("\n==== ")
        h4.insert_after(" ====")

    # Insert "- " in the beginning of list items
    for li in soup.find_all("li"):
        li.insert_before("- ")

    # Append a newline after lists (because conversion from html destroys them for some reason)
    for li in soup.find_all("ul"):
        li.append("\n")
    
    # Remove dangling ',' when words have multiple references
    for sup in soup.find_all("sup", attrs="reference cite_virgule"):
        sup.string = ""

    return soup.get_text()