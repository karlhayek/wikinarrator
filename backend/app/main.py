from typing import List
from io import BytesIO
from pathlib import Path
import re

from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from mediawiki import MediaWiki
import wikipediaapi

from text_cleaner import edit_and_convert_html_text, clean_text, extract_title_from_url

app = FastAPI(version='0.1', title='Wiki Narrator')

wiki = MediaWiki(lang="fr")

wiki_wiki = wikipediaapi.Wikipedia(
    language='fr',
    extract_format=wikipediaapi.ExtractFormat.HTML
    # extract_format=wikipediaapi.ExtractFormat.WIKI
)


@app.get("/api")
async def root():
    return {"Wiki": "trivago"}


class ArticleInfo(BaseModel):
    article_title_or_url: str


@app.post("/api/getarticlecontent")
async def get_article_content_from_title(article_info: ArticleInfo):
    # Get form data
    title_or_url = article_info.article_title_or_url

    # Try to extract title from the URL in the string
    if (url_extract := extract_title_from_url(title_or_url)) != "":
        title = url_extract

    # If extraction from URL fails, then consider input as the title 
    else:
        # Search for title and get first match's url using mediawiki package
        url = ""
        if len(search_results := wiki.opensearch(title_or_url)) == 0:
            return {"page_content": "Error: No articles were found for the given string"}
    
        # Extract title from url
        title = extract_title_from_url(search_results[0][2])


    # print(f"Getting article data for the article: {title} (extracted from {title_or_url})")
    # Retrieve wikipedia page content (in HTML format) using wikipedia-api package
    page = wiki_wiki.page(title)

    # Edit and convert retrieved html text to plaintext
    cleaned_page_text = edit_and_convert_html_text(page.text)
    
    # Clean text
    cleaned_page_text = clean_text(cleaned_page_text)

    # Return the cleaned page text
    return {"page_content": cleaned_page_text}