from typing import List
from io import BytesIO
from pathlib import Path
import re

from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from mediawiki import MediaWiki

from text_cleaner import clean_text

app = FastAPI(version='0.1', title='Wiki Narrator')

wiki = MediaWiki(lang="fr")

@app.get("/api")
async def root():
    return {"Wiki": "trivago"}


class ArticleInfo(BaseModel):
    title: str


@app.post("/api/getarticlecontent")
async def get_article_content_from_title(article_info: ArticleInfo):
    print("Getting article data for title:", article_info.title)
    
    page = wiki.page(article_info.title)
    # page = wiki.page(pageid=3498511)
    
    # cleaned_page_text = clean_text(page.wikitext)
    cleaned_page_text = clean_text(page.content)

    return {"page_content": cleaned_page_text}