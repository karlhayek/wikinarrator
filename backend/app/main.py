from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import pandas as pd
from mediawiki import MediaWiki
import wikipediaapi

from text_cleaner import extract_title_from_url, clean_page_text

app = FastAPI(version='0.1', title='Wiki Narrator')

WIKIPEDIA_SEARCH_API = MediaWiki(lang="fr")

WIKIPEDIA_API = wikipediaapi.Wikipedia(
    language='fr',
    extract_format=wikipediaapi.ExtractFormat.HTML
)


THEMES_DF = pd.read_csv("./data/themes_sous-themes.csv")

# Themes to subthemes dict
THEMES_TO_SUBTHEMES = {theme: sous_themes['Sous-thème'].to_list() for theme, sous_themes in THEMES_DF.groupby("Thème") }


@app.get("/api")
def root():
    return {"Wiki": "API is a-okay"}

class WikiPageResponse(BaseModel):
    page_content: str



@app.get("/api/article/{title_or_url}", response_model=WikiPageResponse)
def get_article_content_from_title(title_or_url: str):
    """ Retrieves Wikipedia page text from a given URL or title. Uses the Wikimedia API to retrieve the text, and cleans and processes
    the generated text in preparation for being sent to a TTS service. The title doesn't have to be exact, as this function searches the input title and returns the first matching page.

    Args:
        title_or_url: str: Path paramether that represents either a Wikipedia page title or URL

    Returns:
        PageResponse: Cleaned and processed page plaintext
    """
    try:
        # Process input, and extract from it the exact wiki page title by using the mediawiki API
        title = get_exact_title(title_or_url)
    except Exception:
        raise HTTPException(status_code=404, detail="No article found for the given string")

    # Retrieve wikipedia page content (in HTML format) using wikipedia-api package (which needs the exact title)
    page = WIKIPEDIA_API.page(title)

    # Convert HTML to text, clean it and prepare it for TTS
    cleaned_page_text  = clean_page_text(page.text)

    # Return the cleaned page text
    return {"page_content": cleaned_page_text}


class ThemesResponse(BaseModel):
    themes_to_subthemes: dict[str, list[str]]


@app.get("/api/themesandsubthemes", response_model=ThemesResponse)
def get_themes_and_subthemes():
    return {"themes_to_subthemes": THEMES_TO_SUBTHEMES}

 

def get_exact_title(title_or_url: str) -> str:
    # Because input is either a page title or a URL, try to extract title from the URL in the string
    if (url_extract := extract_title_from_url(title_or_url)) != "":
        title = url_extract

    # If URL extraction fails, then consider input as the title 
    else:
        # Search for title and get first match's url using mediawiki package
        url = ""
        if len(search_results := WIKIPEDIA_SEARCH_API.opensearch(title_or_url)) == 0:
            raise Exception
    
        # Extract title from url
        title = extract_title_from_url(search_results[0][2])
        if "utilisateur:" in title.lower() or "discussion:" in title.lower():
            raise Exception
    
    return title