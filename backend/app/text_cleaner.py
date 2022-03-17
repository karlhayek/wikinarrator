import re
from functools import lru_cache
from bs4 import BeautifulSoup


class HTMLCleaner():
    def __init__(self, html_text: str):
        # These tags should be new lines. These tags are usually used in citations and sometimes in lists
        html_text = html_text.replace("</dd></dl></dd></dl>", "\n</dd></dl></dd></dl>\n")

        self.soup = BeautifulSoup(html_text, 'html.parser')
        self.cleaned_text: str = None

    def clean_and_convert(self) -> str:
        """ From given html text, clean and process the text and return it converted to HTML """
        self.__clean_headers()
        self.__remove_images_lists()
        self.__correct_lists()
        self.__remove_dangling_references()

        self.cleaned_text = self.soup.get_text()
        
        return self.cleaned_text


    def __clean_headers(self) -> None:
        # Add "="'s in headers
        header_mappings = {"h2": "==","h3": "===","h4": "====",}

        for html_tag, separator in header_mappings.items():
            for element in self.soup.find_all(html_tag):
                element.insert_before(f"\n{separator} ")
                element.insert_after(f" {separator}\n")

    def __remove_images_lists(self) -> None:
        # Remove lists that are of the class "gallery" (list of images)
        for ul in self.soup.select("ul.gallery"):
            ul.extract()    # Remove tag

    def __correct_lists(self) -> None:
        # Insert "- " in the beginning of list items
        for li in self.soup.find_all("li"):
            li.insert_before("- ")

        # Append a newline after lists (because conversion from html destroys them for some reason)
        for li in self.soup.find_all("ul"):
            li.append("\n")

        # Insert the list item number before each item in a ordered list (e.g. "1. ..., 2. ...")
        for ol in self.soup.find_all("ol"):
            item_number = 1
            for li in ol.find_all("li"):
                li.insert_before(f"{item_number}. ")
                item_number += 1

    def __remove_dangling_references(self) -> None:
        # Remove dangling ',' when words have multiple url references
        for sup in self.soup.find_all("sup", attrs="reference cite_virgule"):
            sup.string = ""



# Remove items. Remove all text between brackets ? 
wiki_remove_list = [
    " (en)", "(en) ", "(en)", "[Lequel ?]", "[Lesquel ?]", "[Quoi ?],", "[pas clair]", "[Qui ?]"
]
wiki_remove_list_regex = [
    re.compile(r"\[réf\..+\]"),     # Strings starting with "[ref. ]" or "[source ]""
    re.compile(r"\[source.+\]"),
    re.compile(r"\(\d\d?\)"),       # 2 numbers between parentheses (e.g. '(12)' for references to images)
]
def purge_wiki_text(text: str) -> str:
    """ Remove parts of the cleaned page Wikipedia text that we don't need """
    cleaned_text = text

    # Replace bullet points/lists with numbers 
    # cleaned_text = replace_bullet_points(cleaned_text)=
    for item_to_remove in wiki_remove_list:
        cleaned_text = cleaned_text.replace(item_to_remove, "")
    for regex in wiki_remove_list_regex:
        cleaned_text = regex.sub("", cleaned_text)


    # Remove text at the end of the article (annexes, bibliographies etc.)
    end_sections_to_stop_at = [
        '== Annexes ==', '== Bibliographie ==', '== Notes et références ==', '== Voir aussi ==',
        '== Œuvres ==', '== Publications ==' ##
    ]
    end_pos = get_first_keyword_position(cleaned_text, end_sections_to_stop_at)
    if end_pos != -1:
        cleaned_text = cleaned_text[:end_pos]

    return cleaned_text



TTS_replace_list_regex = {
    re.compile(r"Mc(?=[A-Z][a-z]+)"): "Mac",        # McGellan -> MacGellan
    re.compile(r"(?!\d+)\/(?=\d+)"):  " sur ",    # nombres séparés par '/'
    re.compile(r" \(.+?\)(?! \=\=)"): "",           # Texte between parentheses that isn't a title (doesn't end with at '==')
    re.compile(r"(?<=[1-2]\d\d\d) "): ", "          # Add a coma after a 4-number date
    }

def prepare_text_for_TTS(text: str) -> str:
    """ Prepare text for TTS, removing / replacing characters that are mispronounced by TTS, and adding comas
    to parts of the text to add pauses. """

    # Replace abbreviations
    abbreviations_list = {
        "av. J.-C": "avant Jésus Christ",
    }
    for to_replace, replacer in abbreviations_list.items():
        text = text.replace(to_replace, replacer)

    TTS_replace_list = {
        # " (": ", ",                     # Replace parentheses with comas
        # ") ": ", ",
    }
    for to_replace, replacer in TTS_replace_list.items():
        text = text.replace(to_replace, replacer)
    for regex_to_replace, replacer in TTS_replace_list_regex.items():
        text = regex_to_replace.sub(replacer, text)
    

    # Add comas before these words, to give an additional pause to the TTS
    add_coma_before_list = [
        "mais", "donc", "or", "car", "ou", "parce que"
    ]
    for word in add_coma_before_list:
        text = text.replace(f" {word} ", f", {word} ")
    
    # Add comas before the word preceding these words, to give an additional pause to the TTS
    add_coma_before_prefix_list = [
        "lequel", "laquelle", "lesquels", "lesquelles", 
    ]
    for word in add_coma_before_prefix_list:
        text = re.sub(rf" (?=\S+? {word})", ", ", text)


    # Remove duplicate comas and remove spaces at the beginning and end
    text = text.replace(",, ", ", ").strip()

    return text


@lru_cache(maxsize=20)
def clean_page_text(page_text_html: str) -> str:
    """ Cleans and edits the given wikipedia page HTML and converts it to plaintext.
    Then, edits the text to prepare for TTS.
    Args:
        page_text_html (str): Wikipedia page content in HTML format
    Returns:
        str: Cleaned page text prepared for TTS
    """
    # Edit and convert retrieved html text to plaintext
    cleaned_page_text = HTMLCleaner(page_text_html).clean_and_convert()

    # Clean text from wikitext remnants, removing/replacing wiki markdown
    cleaned_page_text = purge_wiki_text(cleaned_page_text)

    # Edit text to prepare for TTS 
    return prepare_text_for_TTS(cleaned_page_text)




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