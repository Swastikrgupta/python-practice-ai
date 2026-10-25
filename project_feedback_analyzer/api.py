from fastapi import FastAPI 
from pydantic import BaseModel 
from dotenv import load_dotenv
from google import genai
from google.genai import types

from database import init_db, save_review, get_reviews

load_dotenv()

client = genai.Client()

init_db()

app = FastAPI()

class Review(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    label: str
    score: int
    service: str

@app.post("/analyze_review")
def analyze_review(review: Review):
    # Create request to google gemini 3.8 flash model
    response = client.interactions.create(
        model="gemini-3.5-flash-lite",
        system_instruction="You are a helpful assistant that classifies reviews into positive, negative, or neutral categories. Score must be a number from 1 (very bad) to 5 (very good). Service must be ONE lowercase word for the main topic (for example: delivery, taste, price, quality) ",
        input=review.text,
        response_format={
            'type': 'text',
            'mime_type': 'application/json',
            'schema': AnalysisResponse.model_json_schema()
        }
    )

    analysis = AnalysisResponse.model_validate_json(response.output_text)

    # Save the review and its analysis
    save_review(review.text, analysis.label, analysis.score, analysis.service)

    return analysis

@app.get("/reviews")
def list_reviews():
    return get_reviews()
