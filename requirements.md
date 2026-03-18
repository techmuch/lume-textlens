# Requirements Document: Lite-NLP Browser Feedback Workbench (Lume / TextLens)

## Objective
Develop a professional MLOps Jupyter-based environment to prototype and evaluate non-LLM, real-time NLP feedback mechanisms for web-based textareas. The goal is to build a semantic guardrail ("Intent Compliance") that operates in-browser to guide user input, prioritizing extreme efficiency and browser compatibility alongside accuracy. This project acts as a "Vertical Slice," seamlessly transitioning from data generation to an interactive Live Proof of Concept (PoC).

## 1. Technical Stack
- **Environment Manager:** Pixi (Conda/PyPI hybrid).
- **Runtime:** Python 3.11+ within JupyterLab.
- **Core NLP Libraries:** `scikit-learn` (Classical ML), `spacy` (Linguistic features), `sentence-transformers` (Embeddings).
- **UI Simulation:** `ipywidgets` for real-time textarea emulation.
- **Data Generation:** `LiteLLM` or `Ollama` (to generate synthetic testing samples).
- **Testing & Benchmarking:** `pytest`, `pytest-benchmark`, `mlflow` (for experiment tracking).
- **Demo Layer Backend:** `FastAPI`, `uvicorn` for high-performance inference API serving.
- **Demo Layer Frontend:** Vanilla JS, HTML, CSS (Tailwind), `Mark.js` (for visual highlights).

## 2. Functional Requirements

### R1: Synthetic Data Generation (The "Seed")
- The workbench must include a script to generate labeled text samples using an LLM (e.g., GPT-4 or Llama-3).
- **Samples needed:** Professional vs. Casual tone, Passive vs. Active voice, Concise vs. Wordy.
- **Format:** Export to `.jsonl` or `.csv` for easy loading into Pandas.

### R2: The Modeling Workbench (Policy-Based Feedback Strategy)
A three-tier detection strategy for providing in-browser semantic guardrails:

* **Tier 1: Patterns (The Hard No's)**
  * **Use for:** PHI (Social Security Numbers, Phone Numbers, Emails).
  * **Tech:** Optimized Regex and Entity Recognition (NER) using a "lite" Spacy model.
* **Tier 2: Semantic Drift (The "Stay on Topic")**
  * **Use for:** Ensuring a topic doesn't drift (e.g., a "Person Description" shouldn't start talking about "Weather" or "Politics").
  * **Tech:** Compare the Cosine Similarity between the user’s text and a "Target Intent" vector (e.g., words like appearance, biography, traits) using Zero-Shot Classification or Tiny Embeddings (e.g., `all-MiniLM-L6-v2`).
* **Tier 3: Structural Completeness**
  * **Use for:** Ensuring descriptions aren't just one word or lack substance.
  * **Tech:** Heuristics (word count, part-of-speech density).

### R3: Real-Time UI Prototype
- A Jupyter Notebook cell containing a mock text area.
- **Latency Target:** Feedback must update in <100ms per keystroke (simulated via Python `observe` events).
- **Visuals:** Color-coded labels (Green/Yellow/Red) to indicate text quality or style alignment.

### R4: Testing & Evaluation Suite (Three-Tier Hierarchy)
To ensure models are both smart and fast, a three-tier testing approach is required:
* **Unit Tests (Code Integrity):** Ensure preprocessing logic (regex cleaners, tokenizer, vectorizer) does not break when library versions change.
* **Model Tests (Edge Cases):** Target specific "Redline" inputs (e.g., testing that if a user types a Social Security Number, the model always flags it).
* **Experiment Metrics (Performance):** Compare different "Lite" approaches (e.g., Regex vs. SVM vs. Embeddings) against required browser metrics.

### R5: Inference API (Demo Layer)
- A REST endpoint (`/analyze`) served via FastAPI that takes a string input and returns a JSON object containing identified violations, confidence scores, and suggestions.

### R6: Web Interface (Demo Layer)
- A responsive HTML/CSS dashboard for real-time testing.
- **The "X-Ray" View:** A small panel showing the model's Confidence Score and Inference Time (e.g., "Analyzed in 14ms").
- **Instruction Toggle:** A dropdown to change the "Policy" (e.g., "Mode: No-PHI" or "Mode: Person-Focused").
- **Visual Highlights:** Utilize `Mark.js` to highlight exactly where in the text area the violation occurred (e.g., underlining a phone number in red).

### R7: Unit Tested Server (Demo Layer)
- Pytest cases ensuring the API returns the correct HTTP status codes and properly formatted JSON schema.

## 3. Key Metrics for the Workbench
Since models will execute in the browser, "Accuracy" must be balanced against footprint and speed:

| Metric | Why it matters for Browsers |
|---|---|
| **F1-Score** | Balances Precision (not flagging false PHI) and Recall (catching all PHI). |
| **Inference Latency** | Must be < 50ms for "as-you-type" feedback. |
| **Model Payload Size** | Large models (>10MB) slow down page loads. |
| **Memory Footprint** | Low-end mobile browsers will crash if the model uses too much RAM. |

## 4. Proposed "Intent Library" (Testing Samples)
The workbench should generate synthetic data for these specific Use Cases to train and test the models:

| Intent Name | Inclusion Goals (Expectations) | Exclusion Goals (Violations) |
|---|---|---|
| **Biographical** | Physical traits, history, personality. | Addresses, SSNs, medical history (PHI). |
| **Incident Report** | Dates, locations, objective actions. | Emotional rants, hearsay, identifying victim names. |
| **Product Review** | Quality, usability, value. | Shipping complaints, personal attacks, promo links. |
| **Technical Support** | Error codes, steps taken, hardware model. | Passwords, credit card numbers, unrelated small talk. |

## 5. Non-Functional Requirements
- **Portability:** The entire environment must be reproducible via a single `pixi.lock` file.
- **Exportability:** The selected model must be compatible with ONNX or TensorFlow.js for eventual browser deployment.

## 6. Implementation Idea: `pytest-benchmark`
Use `pytest` combined with `pytest-benchmark` to automate the testing suite. 
**Sample Unit Test:**
```python
def test_phi_masking():
    processor = TextProcessor(policy="no-phi")
    input_text = "Call me at 555-0199"
    result = processor.analyze(input_text)
    assert result.has_violation == True
    assert "Phone Number" in result.reason
```

## 7. Pixi Tasks (The "Two-Step" Launch)
The project is configured for a simple "Two-Step" workflow to go from experimentation to presentation:
*   `pixi run workbench` -> Starts the Jupyter Lab environment.
*   `pixi run demo` -> Starts the Live Proof of Concept (FastAPI Server + Frontend).
