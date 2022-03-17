import re
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


    def __clean_headers(self):
        # Add "="'s in headers
        header_mappings = {"h2": "==","h3": "===","h4": "====",}

        for html_tag, separator in header_mappings.items():
            for element in self.soup.find_all(html_tag):
                element.insert_before(f"\n{separator} ")
                element.insert_after(f" {separator}\n")

    def __remove_images_lists(self):
        # Remove lists that are of the class "gallery" (list of images)
        for ul in self.soup.select("ul.gallery"):
            ul.extract()    # Remove tag

    def __correct_lists(self):
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

    def __remove_dangling_references(self):
        # Remove dangling ',' when words have multiple url references
        for sup in self.soup.find_all("sup", attrs="reference cite_virgule"):
            sup.string = ""

    

def clean_text(text: str) -> str:
    """ Remove parts of the cleaned page Wikipedia text that we don't need """
    cleaned_text = text

    # Replace bullet points/lists with numbers 
    # cleaned_text = replace_bullet_points(cleaned_text)

    # Remove items. Remove all text between brackets ? 
    remove_list = [
        " (en)", "(en) ", "(en)", "[Lequel ?]", "[Lesquel ?]", "[Quoi ?],", "[pas clair]", "[Qui ?]"
    ]
    remove_list_regex = [
        r"\[réf\..+\]", r"\[source.+\]", # Strings starting with "[ref. ]" or "[source ]""
        r"\(\d\d?\)",                    # 2 numbers between parentheses (e.g. '(12)' for references to images)
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
    """ Prepare text for TTS, removing / replacing characters that are mispronounced by TTS, and adding comas
    to parts of the text to add pauses. """

    # Replace abbreviations
    abbreviations_list = {
        "av. J.-C": "avant Jésus Christ",
    }
    for to_replace, replacer in abbreviations_list.items():
        text = text.replace(to_replace, replacer)

    replace_list = {
        # " (": ", ",                     # Replace parentheses with comas
        # ") ": ", ",
    }
    replace_list_regex = {
        r"Mc(?=[A-Z][a-z]+)": "Mac",        # McGellan -> MacGellan
        # r"(?!\d+)\/(?=\d+)":  " sur ",    # nombres séparés par '/'
        r" \(.+?\)(?! \=\=)": "",           # Texte between parentheses that isn't a title (doesn't end with at '==')
        r"(?<=[1-2]\d\d\d) ": ", "          # Add a coma after a 4-number date
    }
    for to_replace, replacer in replace_list.items():
        text = text.replace(to_replace, replacer)
    for regex_to_replace, replacer in replace_list_regex.items():
        text = re.sub(regex_to_replace, replacer, text)
    

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



def clean_page_text(page_text_html: str) -> str:
    """ Cleans and edits the given wikipedia page HTML and converts it to plaintext.
    Then, edit the text to prepare for TTS.

    Args:
        page_text_html (str): Wikipedia page content in HTML format

    Returns:
        str: Cleaned page text prepared for TTS
    """
    # Edit and convert retrieved html text to plaintext
    cleaned_page_text = HTMLCleaner(page_text_html).clean_and_convert()

    # Clean text, removing/replacing wiki markdown
    cleaned_page_text = clean_text(cleaned_page_text)

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
