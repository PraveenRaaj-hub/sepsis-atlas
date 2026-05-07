from sentence_transformers import SentenceTransformer
import numpy as np
from ingest import load_all_papers

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks: list[dict]) -> tuple:
    texts = [c['text'] for c in chunks]
    print("Embedding chunks... this takes 1-2 minutes first time")
    embeddings = model.encode(texts, show_progress_bar=True)
    return chunks, embeddings

def retrieve(query: str, chunks: list, embeddings: np.ndarray, top_k: int = 5) -> list[dict]:
    query_embedding = model.encode([query])
    scores = np.dot(embeddings, query_embedding.T).flatten()
    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for i in top_indices:
        result = chunks[i].copy()
        result['score'] = float(scores[i])
        results.append(result)
    return results

if __name__ == "__main__":
    chunks = load_all_papers()
    chunks, embeddings = embed_chunks(chunks)

    query = "What is the relationship between lactate level and 28-day mortality in septic shock?"
    print(f"\nQuery: {query}\n")

    results = retrieve(query, chunks, embeddings)
    for i, r in enumerate(results):
        print(f"--- Result {i+1} | {r['source_file']} | Page {r['page']} | Score: {r['score']:.3f} ---")
        print(r['text'][:300])
        print()