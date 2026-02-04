import sys
import json
from pathlib import Path

from ingest import extract_entities
from relations import extract_relations
from feedback import apply_feedback

DATA_DIR = Path("data")


def ingest_cmd(input_path):
    text = Path(input_path).read_text().strip()
    if not text:
        raise ValueError("input.txt is empty")

    # 1) Entity extraction
    entities = extract_entities(text)

    # 2) Relation extraction
    relations = extract_relations(entities)

    # 3) Optional human feedback
    feedback_path = DATA_DIR / "feedback.json"
    if feedback_path.exists():
        feedback = json.loads(feedback_path.read_text())
        entities, relations = apply_feedback(entities, relations, feedback)

    # 4) Save results
    (DATA_DIR / "entities.json").write_text(json.dumps(entities, indent=2))
    (DATA_DIR / "relations.json").write_text(json.dumps(relations, indent=2))

    print(f"✅ Ingested {len(entities)} entities → data/entities.json")
    print(f"🔗 Extracted {len(relations)} relations → data/relations.json")


def query_cmd(question):
    # Import ONLY when needed (so ingest doesn't load mistral)
    from rag import query_rag

    result = query_rag(question)

    print("\n🧠 Answer:")
    print(result["answer"])

    print("\n🔍 Retrieved Evidence:")
    for e in result["evidence"]:
        print("-", e)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cli.py [ingest|query] <arg>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "ingest":
        ingest_cmd(sys.argv[2])
    elif command == "query":
        query_cmd(sys.argv[2])
    else:
        print("Unknown command")
