from fastapi import FastAPI, Query, HTTPException, Depends
from typing import List
from io import BytesIO
from pathlib import Path

from mediawiki import MediaWiki

app = FastAPI(version='0.1', title='Wiki Narrator')

wiki = MediaWiki(lang="fr")
@app.get("/api")
async def root():
    page = wiki.page('jazz')
    # page = wiki.page(pageid=3498511)

    return {"Summary": page.content}
    # return {"Wiki": "trivago"}

    