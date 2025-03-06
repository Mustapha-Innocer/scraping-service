from pydantic import BaseModel


class SourceArticle(BaseModel):
    url: str
    title: str
    text: str
    timestamp: int
    image: str
    source: str
