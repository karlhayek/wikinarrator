from typing import List
from io import BytesIO
from pathlib import Path
import re

from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from mediawiki import MediaWiki

from text_cleaner import clean_text, extract_title_from_url

app = FastAPI(version='0.1', title='Wiki Narrator')

wiki = MediaWiki(lang="fr")

@app.get("/api")
async def root():
    return {"Wiki": "trivago"}


class ArticleInfo(BaseModel):
    article_title_or_url: str


@app.post("/api/getarticlecontent")
async def get_article_content_from_title(article_info: ArticleInfo):
    print("Getting article data for title/url:", article_info.article_title_or_url)

    # Get form data
    title_or_url = article_info.article_title_or_url

    # Try to extract title from the URL in the string. If it fails then consider the string as the title 
    if (title := extract_title_from_url(title_or_url)) == "":
        title = title_or_url

    # Retrieve wikipedia page content
    page = wiki.page(title)
    # page = wiki.page(pageid=3498511)
    
    # cleaned_page_text = clean_text(page.wikitext)
    cleaned_page_text = clean_text(page.content)

    # Return the cleaned page content
    return {"page_content": cleaned_page_text}