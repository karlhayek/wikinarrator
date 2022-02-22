from fastapi import FastAPI, Query, HTTPException, Depends
from typing import List
from io import BytesIO
from pathlib import Path
from pydantic import BaseModel

from mediawiki import MediaWiki

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

    return {"page_content": page.content}