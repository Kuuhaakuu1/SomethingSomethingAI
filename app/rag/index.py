from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.rag.ingest import DocumentChunk


@dataclass
class RagIndex:
    vectorizer: TfidfVectorizer
    matrix: object
    documents: List[DocumentChunk]

    def search(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        if not query.strip() or not self.documents:
            return []
        query_matrix = self.vectorizer.transform([query])
        scores = cosine_similarity(query_matrix, self.matrix).flatten()
        ranked_indices = scores.argsort()[::-1][:top_k]
        return [self.documents[index] for index in ranked_indices]



def build_index(documents: Iterable[DocumentChunk]) -> RagIndex:
    docs = list(documents)
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([doc.text for doc in docs]) if docs else []
    return RagIndex(vectorizer=vectorizer, matrix=matrix, documents=docs)
