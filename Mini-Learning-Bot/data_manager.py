# bot/data_manager.py
import json
import os
from pathlib import Path
from typing import List, Dict

# Resolve paths relative to project root (../data from this file)
HERE = Path(__file__).resolve().parent
DATA_DIR = (HERE / ".." / "data").resolve()
WORDS_FILE = DATA_DIR / "words.json"
PERF_FILE = DATA_DIR / "performance.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)


# ---------- helpers ----------
def _read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _write_json(path: Path, obj):
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


# ---------- public API ----------
def load_words() -> List[Dict[str, str]]:
    """
    Return a list of {"term": str, "definition": str}.
    Handles legacy formats gracefully.
    """
    data = _read_json(WORDS_FILE, default=[])
    # legacy: dict of term->definition
    if isinstance(data, dict):
        return [{"term": k, "definition": v} for k, v in data.items()]
    # legacy: list of 2-element lists / tuples
    if isinstance(data, list) and data and isinstance(data[0], (list, tuple)) and len(data[0]) == 2:
        return [{"term": t, "definition": d} for t, d in data]
    # expected format
    return data if isinstance(data, list) else []


def save_all_words(words: List[Dict[str, str]]):
    _write_json(WORDS_FILE, words)


def append_word(term: str, definition: str):
    words = load_words()
    # avoid dup term (case insensitive)
    existing_terms = {w["term"].strip().lower(): i for i, w in enumerate(words)}
    key = term.strip().lower()
    if key in existing_terms:
        idx = existing_terms[key]
        words[idx]["definition"] = definition  # update
    else:
        words.append({"term": term, "definition": definition})
    save_all_words(words)


def load_performance():
    return _read_json(PERF_FILE, default={"sessions": []})


def save_performance(data):
    _write_json(PERF_FILE, data)
