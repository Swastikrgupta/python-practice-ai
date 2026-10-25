import os

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
from functools import lru_cache


load_dotenv()

try:
    from google import genai
except ImportError:  # pragma: no cover - optional dependency
    genai = None


@lru_cache
def get_client():
    if genai is None:
        raise RuntimeError("Install the 'google-genai' package to use Gemini.")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Set the GOOGLE_API_KEY environment variable.")

    return genai.Client(api_key=api_key)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Review(BaseModel):
    text: str


class Sentiment(BaseModel):
    label: Literal['positive', 'negative']
    score: int = Field(ge=1, le=5, description="Strength of the sentiment, 1-5")


@app.post("/sentiment")
def sentiment_analysis(review: Review):
    interaction = get_client().interactions.create(
        model='gemini-3.8-flash',
        system_instruction=(
            'You are a sentiment analysis model. Classify the customer review as '
            '"positive" or "negative" and score the strength of the sentiment from 1 to 5.'
        ),
        input = review.text,
        response_format = {
            'type': 'text',
            'mime_type': 'application/json',
            'schema': Sentiment.model_json_schema()
        }
    )

    return Sentiment.model_validate_json(interaction.output_text)
    