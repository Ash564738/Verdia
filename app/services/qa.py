from __future__ import annotations


class EnglishPlantQA:
    """Small local QA baseline; replace with embeddings + vector DB in production."""

    _knowledge = {
        "watering": (
            "Water the plant when the top layer of soil is dry. Avoid standing water "
            "around the roots and improve drainage.",
            "Plant health care guide",
        ),
        "blight": (
            "Remove affected leaves, keep foliage dry, improve airflow, and follow a "
            "locally approved fungicide label when necessary.",
            "Plant disease management guide",
        ),
        "scab": (
            "Prune infected material, remove fallen leaves, and reduce prolonged leaf "
            "wetness to slow scab development.",
            "Plant disease management guide",
        ),
    }

    def answer(self, question: str) -> dict[str, list[str] | str]:
        normalized = question.lower()
        if "water" in normalized:
            answer, source = self._knowledge["watering"]
            return {"answer": answer, "sources": [source]}
        for keyword, (answer, source) in self._knowledge.items():
            if keyword in normalized:
                return {"answer": answer, "sources": [source]}
        return {
            "answer": (
                "I can help with watering, blight, and scab at the moment. "
                "Please describe the plant and visible symptoms in English."
            ),
            "sources": ["Plant health care guide"],
        }
