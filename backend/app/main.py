from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from mediawiki import MediaWiki
import wikipediaapi

from text_cleaner import extract_title_from_url, clean_page_text

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

    try:
        # Process input, and extract from it the exact wiki page title by using the mediawiki API
        title = get_exact_title(title_or_url)
    except Exception:
        return {"page_content": "Error: No articles were found for the given string"}

    # Retrieve wikipedia page content (in HTML format) using wikipedia-api package (which needs the exact title)
    page = wiki_wiki.page(title)

    # Convert HTML to text, clean it and prepare it for TTS
    cleaned_page_text  = clean_page_text(page.text)

    # Return the cleaned page text
    return {"page_content": cleaned_page_text}

 

def get_exact_title(title_or_url: str) -> str:
    # Because input is either a page title or a URL, try to extract title from the URL in the string
    if (url_extract := extract_title_from_url(title_or_url)) != "":
        title = url_extract

    # If URL extraction fails, then consider input as the title 
    else:
        # Search for title and get first match's url using mediawiki package
        url = ""
        if len(search_results := wiki.opensearch(title_or_url)) == 0:
            raise Exception
    
        # Extract title from url
        title = extract_title_from_url(search_results[0][2])
        if "utilisateur:" in title.lower() or "discussion:" in title.lower():
            raise Exception
    
    return title