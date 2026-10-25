# Python Practice: AI

My notes and small projects from learning Python and building apps with Google Gemini.

## What's inside

| Path | What it is |
| --- | --- |
| `dataTypes-Loops-classes.ipynb` | Python basics: data types, loops and classes |
| `Error_handling.ipynb` | Handling errors with try/except |
| `File_handling.ipynb` | Reading and writing files |
| `call_llm.ipynb` | First calls to the Gemini API |
| `context_memory.ipynb` | Giving an LLM chat memory |
| `chat_app.py` | Streamlit chat app using Gemini |
| `recipe_app.py` | Streamlit app that suggests recipes from your ingredients |
| `Fast_API/` | A small FastAPI backend that calls Gemini |
| `project_feedback_analyzer/` | Full project: review analysis with FastAPI, Gemini, SQLite and Streamlit ([README](project_feedback_analyzer/README.md)) |

## Running the apps

```bash
pip install -r requirements.txt
cp .env.example .env   # then add your Gemini API key
streamlit run chat_app.py
```

Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).
