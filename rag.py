import json
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from llm import explain_answer

DATA_DIR = Path("data")

# Load embedding model once
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def load_entities():
    path = DATA_DIR / "entities.json"
    if not path.exists():
        raise FileNotFoundError("entities.json not found. Run ingest first.")
    return json.loads(path.read_text())


def retrieve_evidence(question: str, top_k: int = 5):
    entities = load_entities()

    if not entities:
        return []

    corpus = [
        f"{e.get('text')} ({e.get('type')}): {e.get('sentence', '')}"
        for e in entities
    ]

    corpus_embeddings = embed_model.encode(corpus, convert_to_tensor=True)
    question_embedding = embed_model.encode(question, convert_to_tensor=True)

    scores = util.cos_sim(question_embedding, corpus_embeddings)[0]
    k = min(top_k, len(corpus))
    top_results = scores.topk(k=k)

    evidence = [corpus[int(i)] for i in top_results.indices]
    return evidence


def query_rag(question: str):
    evidence = retrieve_evidence(question, top_k=5)

    if not evidence:
        return {
            "question": question,
            "evidence": [],
            "answer": "No evidence found. Run ingest first or provide biomedical text."
        }

    answer = explain_answer(question, "\n".join(evidence))

    return {
        "question": question,
        "evidence": evidence,
        "answer": answer
    }
