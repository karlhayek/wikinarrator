import re
import urllib
import mwparserfromhell

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


def clean_text(wiki_text: str):
    # Wiki text processing
    # # Replace bullet points/lists with numbers 
    # wiki_text = replace_bullet_points(wiki_text)

    # # Convert wikitext to plain text
    # plain_text = mwparserfromhell.parse(wiki_text).strip_code()

    # Post-processing on the text converted from wikitext
    # cleaned_text = plain_text
    cleaned_text = wiki_text


    # Remove items
    remove_list = [
        " (en)", "(en) ", "[réf. nécessaire]", "[Lequel ?]", "[Lesquel ?]", "[Quoi ?],", "[pas clair]", "[réf. souhaitée]"
    ]
    for item_to_remove in remove_list:
        cleaned_text = cleaned_text.replace(item_to_remove, "")

    # Replace items
    replace_list = {
        "(": ", ",
        ")": ", "
    }
    for to_replace, replacer in replace_list.items():
        cleaned_text = cleaned_text.replace(to_replace, replacer)

    
    # Remove text at the end of the article (annexes, bibliographies etc.)
    end_pos = get_first_keyword_position(cleaned_text, ['== Annexes ==', '== Bibliographie ==', '== Notes et références ==', '== Voir aussi =='])
    if end_pos != -1:
        cleaned_text = cleaned_text[:end_pos]

    return cleaned_text



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