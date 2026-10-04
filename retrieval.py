"""
TF-IDF-based retrieval over the hiring-reality knowledge base.
Same core approach as AgriBot: vectorize the query (the JD text), vectorize
the knowledge base, rank by cosine similarity, and only surface KB entries
that are genuinely relevant rather than dumping the whole KB into the prompt.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from knowledge_base import KNOWLEDGE_BASE


class KnowledgeRetriever:
    def __init__(self, knowledge_base=None, min_similarity: float = 0.03):
        self.kb = knowledge_base or KNOWLEDGE_BASE
        self.min_similarity = min_similarity
        self._texts = [entry["text"] for entry in self.kb]
        self._vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self._matrix = self._vectorizer.fit_transform(self._texts)

    def retrieve(self, query_text: str, top_k: int = 6):
        """Return the top_k most relevant KB entries for a given JD text,
        each annotated with its similarity score. Entries below
        min_similarity are dropped so weakly-related patterns aren't forced
        into the analysis."""
        query_vec = self._vectorizer.transform([query_text])
        sims = cosine_similarity(query_vec, self._matrix).flatten()

        ranked_idx = np.argsort(sims)[::-1][:top_k]
        results = []
        for idx in ranked_idx:
            score = float(sims[idx])
            if score < self.min_similarity:
                continue
            entry = dict(self.kb[idx])
            entry["similarity"] = round(score, 4)
            results.append(entry)
        return results
