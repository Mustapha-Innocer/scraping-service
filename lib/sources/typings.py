from pydantic import BaseModel


class ScrapedData(BaseModel):
    url: str
    title: str
    body: str
    timestamp: int
    image_url: str
    source: str
    author: str