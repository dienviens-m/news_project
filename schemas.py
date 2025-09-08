from typing import List

from pydantic import BaseModel, Field

class NewsItem(BaseModel):
    """schema for news item with title and url"""
    title: str = Field(description="The title of the news")
    url: str = Field(description="The URL of the source")

class NewsResponse(BaseModel):
    """schema for news response with results"""
    results: List[NewsItem] = Field(
        default_factory=list, description="List of news item"
    )
