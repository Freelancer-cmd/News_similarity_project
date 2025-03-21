from fastapi import FastAPI
from Data.dataset import NewsSearchEngine
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="News Search API")

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

search_engine = NewsSearchEngine()
search_engine.load_index()


# Request model
class SearchRequest(BaseModel):
    queryText: str = "test query"
    top_k: int = 10

@app.post("/search")
async def search(request: SearchRequest):
    return {
        "query": request.queryText,
        "results": search_engine.search(request.queryText, request.top_k)
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "News Search API is running!"}