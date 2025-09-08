from fastapi import APIRouter
from pydantic import BaseModel, Field
from agent import news_search

router = APIRouter()

class NewsRequest(BaseModel):
    input: str = Field(min_length=3)

@router.post("/search")
async def search_news(request:NewsRequest):
    result = news_search(request.input)
    return result