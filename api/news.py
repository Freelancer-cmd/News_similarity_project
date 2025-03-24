from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Model.relevant_news import search_relevant_articles

app = FastAPI(title="News Search API")

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model
class SearchRequest(BaseModel):
    queryText: str
    topK: int

@app.post("/search")
async def search(request: SearchRequest):
    return {
        "query": request.queryText,
        "results": search_relevant_articles(request.queryText, request.topK)
    }