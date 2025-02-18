from pydantic import BaseModel

class Article(BaseModel):
    title: str
    author: str
    content: str
    images: list[str] = []
    version: int = 1