from pydantic import BaseModel


class SourceArticle(BaseModel):
    url: str
    title: str
    category: str
    text: str
    timestamp: int
    image_url: str
    source: str
