from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn
import re
from contextlib import asynccontextmanager

df = None
tfidf_matrix = None
vectorizer = None

def load_and_preprocess_data():
    global df, tfidf_matrix, vectorizer
    print("🔄 Initializing resources...")
    df = pd.read_csv("product_catalog.csv")
    df.dropna(subset=["description"], inplace=True)
    df.fillna("", inplace=True)

    corpus = df["description"] + " " + df["test_type"] + " " + df["url"]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)

    print("✅ Resources initialized.")

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_and_preprocess_data()
    yield

app = FastAPI(lifespan=lifespan)

class QueryRequest(BaseModel):
    query: str

class AssessmentResponse(BaseModel):
    url: str
    adaptive_support: str
    description: str
    duration: int
    remote_support: str
    test_type: List[str]

@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

def clean_query(query: str) -> str:
    query = query.strip()  
    query = re.sub(r'\s+', ' ', query) 
    return query

@app.post("/recommend")
async def recommend_assessments(request: QueryRequest) -> Dict[str, List[AssessmentResponse]]:  
    query = request.query.strip() 
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[::-1][:10]

    recommended = []
    for idx in top_indices:
        if similarities[idx] == 0:
            continue
        item = df.iloc[idx]
        recommended.append({
            "url": item["url"],
            "adaptive_support": item["adaptive_support"],
            "description": item["description"],
            "duration": int(item["duration"]),
            "remote_support": item["remote_support"],
            "test_type": [t.strip() for t in str(item["test_type"]).split(",") if t.strip()]
        })

    if not recommended:
        recommended.append({
            "url": "",
            "adaptive_support": "No",
            "description": "No relevant assessment found.",
            "duration": 0,
            "remote_support": "No",
            "test_type": []
        })

    return {"recommended assessments": recommended}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
