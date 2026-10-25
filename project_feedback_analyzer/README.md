# Feedback Analyzer

Analyzes customer reviews with Google Gemini. For each review it returns:

- **label**: `positive`, `negative` or `neutral`
- **score**: 1 (very bad) to 5 (very good)
- **service**: the main topic, as one lowercase word (for example `delivery`, `taste`, `price`)

Every analyzed review is saved to a SQLite database, and a Streamlit page lets you analyze new reviews and browse past ones.

## Tech stack

- **FastAPI** backend: [api.py](api.py)
- **Google Gemini** (`google-genai`) with structured JSON output
- **SQLite** storage: [database.py](database.py)
- **Streamlit** frontend: [app.py](app.py)
- **uv** for dependencies, with Python 3.14

## Setup

1. Install [uv](https://docs.astral.sh/uv/), then install the dependencies:

   ```bash
   uv sync
   ```

2. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) and add it to a `.env` file in the project folder:

   ```
   GEMINI_API_KEY=your-key-here
   ```

## Running

Start the backend and the frontend in two terminals:

```bash
# Terminal 1: API on http://localhost:8000 (interactive docs at /docs)
uv run fastapi dev api.py

# Terminal 2: web app on http://localhost:8501
uv run streamlit run app.py
```

The frontend expects the API on port 8000.

## Using the app

- **Analyze** tab: paste a review and click **Analyze** to see its label, score and service.
- **History** tab: see every saved review, the total count, the average score and the percentage of positive reviews.

[sample_reviews.txt](sample_reviews.txt) has example reviews to try.

## API

### `POST /analyze_review`

Analyzes a review and saves the result.

```bash
curl -X POST http://localhost:8000/analyze_review \
  -H "Content-Type: application/json" \
  -d '{"text": "The food was delicious but the delivery took over an hour. Not happy."}'
```

```json
{ "label": "negative", "score": 2, "service": "delivery" }
```

### `GET /reviews`

Returns all saved reviews, newest first.

```json
[
  {
    "id": 1,
    "text": "The food was delicious but the delivery took over an hour. Not happy.",
    "label": "negative",
    "score": 2,
    "service": "delivery",
    "created_at": "2026-10-04 20:39:57"
  }
]
```

## Database

Reviews are stored in `reviews.db`, a SQLite file that is created automatically the first time the API starts. It is listed in `.gitignore`, so it isn't committed. To look at the data directly:

```bash
sqlite3 reviews.db "SELECT * FROM reviews;"
```

To start fresh, stop the API and delete `reviews.db`.

## Project structure

```
.
├── api.py               # FastAPI app and Gemini call
├── database.py          # SQLite setup, insert and query
├── app.py               # Streamlit frontend
├── sample_reviews.txt   # Example reviews
└── pyproject.toml       # Dependencies
```
