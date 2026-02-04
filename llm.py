from pathlib import Path
from llama_cpp import Llama

# ✅ Use Phi-2 model (since your Mistral file is 0 bytes)
MODEL_PATH = Path("models/phi-2.Q4_K_M.gguf")

if not MODEL_PATH.exists() or MODEL_PATH.stat().st_size == 0:
    raise FileNotFoundError(
        f"Model file not found or empty: {MODEL_PATH}\n"
        "Make sure your GGUF model is downloaded correctly."
    )

# Load the model once (global)
llm = Llama(
    model_path=str(MODEL_PATH),
    n_ctx=2048,
    n_threads=8,   # You can increase (like 6 or 8) if your CPU supports
    verbose=False
)


def explain_answer(question: str, evidence: str) -> str:
    """
    Generates final answer using local Phi-2 model.
    """

    prompt = f"""
You are a biomedical assistant.

Answer the question ONLY using the evidence below.
If the evidence does not contain the answer, say:
"I don't know based on the provided evidence."

Evidence:
{evidence}

Question:
{question}

Answer:
""".strip()

    output = llm(
        prompt,
        max_tokens=256,
        temperature=0.2,
        top_p=0.9,
        stop=["\n\n", "Evidence:", "Question:"]
    )

    return output["choices"][0]["text"].strip()
