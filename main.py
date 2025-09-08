from fastapi import FastAPI
import schemas
from routers import news

app = FastAPI()

app.include_router(news.router)
