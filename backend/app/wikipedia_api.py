import re
import urllib
from mediawiki import MediaWiki
import wikipediaapi


WIKIPEDIA_SEARCH_API = MediaWiki(lang="fr")

WIKIPEDIA_API = wikipediaapi.Wikipedia(
    language='fr',
    extract_format=wikipediaapi.ExtractFormat.HTML
    # extract_format=wikipediaapi.ExtractFormat.TEXT
)


def get_exact_title(title_or_url: str) -> str:
    # Because input is either a page title or a URL, try to extract title from the URL in the string
    if (url_extract := extract_title_from_url(title_or_url)) != "":
        title = url_extract

    # If URL extraction fails, then consider input as the title 
    else:
        # Search for title and get first match's url using mediawiki package
        url = ""
        if len(search_results := WIKIPEDIA_SEARCH_API.opensearch(title_or_url)) == 0:
            # No article found in the search
            raise Exception
    
        # Extract title from url
        title = extract_title_from_url(search_results[0][2])
        if "utilisateur:" in title.lower() or "discussion:" in title.lower():
            # An article wasn't found, and instead the search returns a wikipedia user or discussion
            raise Exception
    
    return title

def get_article_content(title: str) -> str:
    """ Retrieves wikipedia page content (in HTML format) using wikipedia-api package (which needs the exact title)
    Args:
        title (str): Exact title of the article we'd like to get the content from
    Returns:
        str: Article page content
    """
    return WIKIPEDIA_API.page(title)


title_extract_regex = re.compile(r"(?<=https:\/\/\S\S\.wikipedia\.org\/wiki.)\S+[^#]$")

def extract_title_from_url(url: str) -> str:
    """ Extracts wikipedia article title from a URL. Example: "https://fr.wikipedia.org/wiki/Hedy_Lamarr" returns "Hedy_Lamarr" """
    # Extract title from the URL using a regex
    # ex: from "https://fr.wikipedia.org/wiki/Grandes_d%C3%A9couvertes#Contexte" we get "Grandes_d%C3%A9couvertes#Contexte"
    matches = title_extract_regex.findall(url)
    if len(matches) == 0:
        # raise Exception("URL is invalid ! Make sure it is a valid wikipedia article URL")
        return ""
    
    # Sanitize title extracted from the URL
    title = urllib.parse.unquote(matches[0], encoding='utf-8', errors='replace')

    # Remove possible '#' suffix to the URl (ex: from a wiki section)
    title = title.split('#')[0]

    return title
