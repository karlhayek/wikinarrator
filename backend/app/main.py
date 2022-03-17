from fastapi import FastAPI, Query, HTTPException
import csv
from collections import defaultdict

import text_cleaner
import wikipedia_api
from response_models import *
import text_highlighter

app = FastAPI(version='0.2', title='Wiki Narrator')


# Themes to subthemes dict
themes_csv = csv.DictReader(open("./data/themes_sous-themes.csv"))
THEMES_TO_SUBTHEMES = defaultdict(list)
for row in themes_csv:
    THEMES_TO_SUBTHEMES[row['Thème']].append(row['Sous-thème'])



@app.get("/api")
def root():
    return {"Wiki": "API is a-okay"}


@app.get("/api/article/", response_model=WikiPageResponse)
def get_article_content_from_title(title_or_url: str) -> WikiPageResponse:
    """ Retrieves Wikipedia page text from a given URL or title. Uses the Wikimedia API to retrieve the text, and cleans and processes
    the generated text in preparation for being sent to a TTS service. The title doesn't have to be exact, as this function searches the input title and returns the first matching page.

    Args:
        title_or_url: str: Query paramether that represents either a Wikipedia page title or URL

    Returns:
        PageResponse: Cleaned and processed page plaintext
    """
    try:
        # Process input, and extract from it the exact wiki page title by using the mediawiki API
        title = wikipedia_api.get_exact_title(title_or_url)

    except Exception as E:
        print("Error occured:", E)
        raise HTTPException(status_code=404, detail="No article found for the given string")

    # Retrieve wikipedia page content (in HTML format) using wikipedia-api package (which needs the exact title)
    page = wikipedia_api.get_article_content(title)

    # Convert HTML to text, clean it and prepare it for TTS
    cleaned_page_text = text_cleaner.clean_page_text(page.text)

    highlighted_text = text_highlighter.highlight_text(cleaned_page_text)

    # Return the cleaned page text
    return {"page_content": highlighted_text}


@app.get("/api/themesandsubthemes", response_model=ThemesResponse)
def get_themes_and_subthemes() -> ThemesResponse:
    """ Returns themes to subthemes mapping """
    return {"themes_to_subthemes": THEMES_TO_SUBTHEMES}