# Biomedical RAG Demo (Local)

A lightweight **Biomedical Retrieval-Augmented Generation (RAG)** pipeline that:
- extracts biomedical entities from text using **SciSpacy**
- retrieves relevant evidence using **sentence embeddings** (`all-MiniLM-L6-v2`) + **cosine similarity**
- generates answers using a **local GGUF LLM** via `llama-cpp-python` (Phi-2)

---

##  Features

 1. Biomedical entity extraction (SciSpacy `en_ner_bc5cdr_md`)  
 2. Stores extracted entities in JSON  
 3. Retrieval using embeddings + cosine similarity  
 4. Local LLM answer generation (GGUF model)  
 5. Optional human feedback support (corrections, removals, relation additions)

---

## 📂 Project Structure

biomedical_rag_demo/
│
├── cli.py

├── ingest.py

├── rag.py

├── llm.py

├── feedback.py

├── relations.py
│

├── data/

│ ├── input.txt

│ ├── entities.json

│ ├── relations.json

│ └── feedback.json (optional)
│

└── models/

├── phi-2.Q4_K_M.gguf

-------

---

##  Setup

### 1. Install Dependencies
pip install -r requirements.txt

------
### 2. Download a GGUF model
This model uses Phi-2

phi-2.Q4_K_M.gguf
_________________
### 3. Usage

Step 1: Put biomedical text in data/input.txt

Example:

Metformin is commonly used for diabetes treatment.
Insulin is another drug used in diabetes.

Step 2: Run ingestion
python cli.py ingest data/input.txt


This generates:

data/entities.json

data/relations.json

Step 3: Ask a question
python cli.py query "Which drugs are associated with diabetes?"

## How it Works
1. Ingestion

SciSpacy extracts biomedical entities like DISEASE, CHEMICAL

Saves them with the sentence context

2. Retrieval

Converts entities into retrievable sentences

Embeds them using all-MiniLM-L6-v2

Retrieves top evidence using cosine similarity

3. Generation

Evidence is passed to the local LLM

LLM answers only using retrieved evidence

Human Feedback (Optional)

We can manually create data/feedback.json:

{
  "remove_entities": [],
  "correct_entities": [
{
      "original": "Herceptin",
      "corrected": "Trastuzumab",
      "label": "DRUG"
    }
],
  "add_relations": []
}


If present, feedback is applied during ingest.

Author

Sanjukta Bag


---

