from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nltk.tokenize import sent_tokenize, word_tokenize
import uvicorn
import json
import uuid
from datetime import datetime
from pathlib import Path

from python_algo import main as python_main
from sumy_lib_based_summary import main as sumy_main
from transformers_based_summary import main as transformers_main
from text_cleaner import clean_text

app = FastAPI(title="Text Summarization API")

# Allow CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production make sure to restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- History Storage ---
HISTORY_DIR = Path(__file__).parent / "history"
HISTORY_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = HISTORY_DIR / "history.json"


def _load_history() -> list:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_history(history: list):
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


# --- Request Models ---
class SummarizeRequest(BaseModel):
    text: str
    model_selection: str
    no_of_sentence_on_output: int = 2


class CleanRequest(BaseModel):
    text: str


# --- Model name mapping for display ---
MODEL_LABELS = {
    "Core Python algo(Frequency and Ranking based)": "TF-IDF Algorithm",
    "Lex Rank: From Python lib sumy": "Sumy: Lex Rank",
    "LSA: From Python lib sumy": "Sumy: LSA",
    "Text Rank: From Python lib sumy": "Sumy: Text Rank",
    "AI Contextual (Deep Learning)": "BART LLM",
}


@app.post("/summarize")
def summarize_text(req: SummarizeRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        if req.model_selection == "Core Python algo(Frequency and Ranking based)":
            summary = python_main(text=req.text, sentence_on_output=req.no_of_sentence_on_output)
        elif req.model_selection == "Lex Rank: From Python lib sumy":
            summary = sumy_main(text=req.text, model_name="Lex Rank", sentence_on_output=req.no_of_sentence_on_output)
        elif req.model_selection == "LSA: From Python lib sumy":
            summary = sumy_main(text=req.text, model_name="LSA", sentence_on_output=req.no_of_sentence_on_output)
        elif req.model_selection == "Text Rank: From Python lib sumy":
            summary = sumy_main(text=req.text, model_name="Text Rank", sentence_on_output=req.no_of_sentence_on_output)
        elif req.model_selection == "AI Contextual (Deep Learning)":
            # For Deep Learning, we dynamically map the user's sentence preference 
            # to a rough max_length token count (e.g., 1 sentence * ~25 words * ~1.3 tokens)
            max_len = max(40, req.no_of_sentence_on_output * 35)
            min_len = max(10, req.no_of_sentence_on_output * 15)
            summary = transformers_main(text=req.text, max_length=max_len, min_length=min_len)
        else:
            raise HTTPException(status_code=400, detail="Invalid model selection")

        # Compute metadata
        original_words = len(word_tokenize(req.text))
        summary_words = len(word_tokenize(summary)) if summary else 0
        summary_sentences = len(sent_tokenize(summary)) if summary else 0
        compression = round((1 - summary_words / max(original_words, 1)) * 100, 1)

        meta = {
            "original_words": original_words,
            "summary_words": summary_words,
            "summary_sentences": summary_sentences,
            "compression_ratio": compression,
        }

        # Save to history
        history = _load_history()
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "model": MODEL_LABELS.get(req.model_selection, req.model_selection),
            "input_preview": req.text[:150].strip(),
            "summary": summary.strip(),
            "meta": meta,
        }
        history.insert(0, entry)  # newest first
        # Keep last 50 entries
        history = history[:50]
        _save_history(history)

        return {
            "summary": summary.strip(),
            "meta": meta,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clean")
def clean_input(req: CleanRequest):
    """Preview the text after preprocessing — useful for debugging."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    cleaned = clean_text(req.text)
    return {"cleaned_text": cleaned}


# --- History Endpoints ---
@app.get("/history")
def get_history():
    """Return all saved history entries, newest first."""
    return _load_history()


@app.delete("/history/{entry_id}")
def delete_history_entry(entry_id: str):
    """Delete a single history entry by ID."""
    history = _load_history()
    new_history = [h for h in history if h["id"] != entry_id]
    if len(new_history) == len(history):
        raise HTTPException(status_code=404, detail="Entry not found")
    _save_history(new_history)
    return {"status": "deleted"}


@app.delete("/history")
def clear_history():
    """Clear all history entries."""
    _save_history([])
    return {"status": "cleared"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
