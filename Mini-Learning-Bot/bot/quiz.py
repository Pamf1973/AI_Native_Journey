# bot/quiz.py
from typing import List, Dict, Optional
import random

class Quiz:
    """
    Simple quiz engine that works with a list of dicts:
    [{"term": "...", "definition": "..."}, ...]
    """
    def __init__(self, items: List[Dict[str, str]], shuffle: bool = True):
        self.items = items[:]  # copy
        if shuffle:
            random.shuffle(self.items)
        self.index = 0
        self.correct = 0
        self.incorrect = 0

    # ---------- metadata ----------
    def total(self) -> int:
        return len(self.items)

    def progress_fraction(self) -> float:
        if self.total() == 0:
            return 0.0
        return self.index / self.total()

    # ---------- question access ----------
    def current(self) -> Optional[Dict[str, str]]:
        if 0 <= self.index < self.total():
            return self.items[self.index]
        return None

    def current_term(self) -> Optional[str]:
        cur = self.current()
        return cur["term"] if cur else None

    def current_definition(self) -> Optional[str]:
        cur = self.current()
        return cur["definition"] if cur else None

    # ---------- answer checking ----------
    def check(self, user_answer: str) -> bool:
        """Return True if correct; False otherwise. Increments counters."""
        correct_def = self.current_definition() or ""
        is_correct = user_answer.strip().lower() == correct_def.strip().lower()
        if is_correct:
            self.correct += 1
        else:
            self.incorrect += 1
        return is_correct

    # ---------- advance ----------
    def next(self) -> bool:
        """
        Move to next question. Returns True if moved to a new question,
        False if we are past the end.
        """
        self.index += 1
        return self.index < self.total()

    # ---------- reset ----------
    def reset(self, shuffle: bool = True):
        self.index = 0
        self.correct = 0
        self.incorrect = 0
        if shuffle:
            random.shuffle(self.items)


