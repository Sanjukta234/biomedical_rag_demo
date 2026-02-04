import spacy
from typing import List, Dict

# Biomedical NER model
nlp = spacy.load("en_ner_bc5cdr_md")


def extract_entities(text: str) -> List[Dict]:
    """
    Extracts biomedical entities using spaCy BC5CDR model.
    Returns list of dicts:
    [
      {
        "text": "...",
        "type": "DISEASE" or "CHEMICAL",
        "sentence": "...",
        "confidence": 0.95
      }
    ]
    """

    doc = nlp(text)

    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text.strip(),
            "type": ent.label_,  # CHEMICAL or DISEASE
            "sentence": ent.sent.text.strip(),
            "confidence": 0.95
        })

    return entities
