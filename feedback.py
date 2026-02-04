from typing import List, Dict, Tuple, Any


def apply_feedback(
    entities: List[Dict],
    relations: List[Dict],
    feedback: Any
) -> Tuple[List[Dict], List[Dict]]:
    """
    feedback schema:
    {
      "remove_entities": ["tumor"],
      "correct_entities": [
        {
          "original": "Herceptin",
          "corrected": "Trastuzumab",
          "type": "CHEMICAL"
        }
      ],
      "add_relations": [
        {
          "head": "Trastuzumab",
          "relation": "TARGETS",
          "tail": "HER2 receptor",
          "evidence": "Trastuzumab binds to HER2 receptor."
        }
      ]
    }
    """

    # Safety: feedback may accidentally be a list
    if isinstance(feedback, list):
        feedback = feedback[0] if feedback else {}

    if not isinstance(feedback, dict):
        return entities, relations

    # 1) Remove entities
    remove_list = set(feedback.get("remove_entities", []))
    entities = [e for e in entities if e.get("text") not in remove_list]

    # 2) Correct entities
    for corr in feedback.get("correct_entities", []):
        original = corr.get("original")
        corrected = corr.get("corrected")
        corrected_type = corr.get("type")

        if not original or not corrected:
            continue

        for e in entities:
            if e.get("text") == original:
                e["text"] = corrected
                if corrected_type:
                    e["type"] = corrected_type

    # 3) Add relations
    relations = relations + feedback.get("add_relations", [])

    return entities, relations
