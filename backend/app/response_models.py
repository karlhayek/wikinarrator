from pydantic import BaseModel


class WikiPageResponse(BaseModel):
    page_content: str


class ThemesResponse(BaseModel):
    themes_to_subthemes: dict[str, list[str]]
