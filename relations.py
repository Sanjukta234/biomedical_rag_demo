from typing import List, Dict


def extract_relations(entities: List[Dict]) -> List[Dict]:
    """
    Very simple rule-based relation extraction:
    If a CHEMICAL and a DISEASE appear in the same sentence,
    we create a relation: TREATS

    Output:
    [
      {
        "head": "Metformin",
        "relation": "TREATS",
        "tail": "diabetes",
        "evidence": "Metformin is commonly used for diabetes treatment."
      }
    ]
    """

    relations = []

    chemicals = [e for e in entities if e.get("type") == "CHEMICAL"]
    diseases = [e for e in entities if e.get("type") == "DISEASE"]

    for chem in chemicals:
        for dis in diseases:
            if chem.get("sentence") == dis.get("sentence"):
                relations.append({
                    "head": chem["text"],
                    "relation": "TREATS",
                    "tail": dis["text"],
                    "evidence": chem["sentence"]
                })

    return relations
