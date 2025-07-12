from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from typing import Optional

app = FastAPI()

def init_db():
    with sqlite3.connect("reviews.db") as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                created_at TEXT NOT NULL
            )"""
        )
        conn.commit()

init_db()

class ReviewRequest(BaseModel):
    text: str

class ReviewResponse(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str

def analyze_sentiment(text: str) -> str:
    text_lower = text.lower()
    positive_words = ["хорош", "отличн", "прекрасн", "люблю", "нравится", "супер", "класс"]
    negative_words = ["плох", "ужасн", "ненавиж", "отвратительн", "кошмар", "разочарован"]
    
    if any(word in text_lower for word in positive_words):
        return "positive"
    elif any(word in text_lower for word in negative_words):
        return "negative"
    else:
        return "neutral"

@app.post("/reviews", response_model=ReviewResponse)
async def create_review(review: ReviewRequest):
    sentiment = analyze_sentiment(review.text)
    created_at = datetime.utcnow().isoformat()
    
    with sqlite3.connect("reviews.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
            (review.text, sentiment, created_at)
        )
        review_id = cursor.lastrowid
        conn.commit()
    
    return {
        "id": review_id,
        "text": review.text,
        "sentiment": sentiment,
        "created_at": created_at
    }

@app.get("/reviews", response_model=list[ReviewResponse])
async def get_reviews(sentiment: Optional[str] = None):
    query = "SELECT id, text, sentiment, created_at FROM reviews"
    params = ()
    
    if sentiment:
        query += " WHERE sentiment = ?"
        params = (sentiment,)
    
    with sqlite3.connect("reviews.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        reviews = cursor.fetchall()
    
    return [dict(review) for review in reviews]