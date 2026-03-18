# Developer Guide: Lite-NLP Workbench

Welcome to the IntentGate / FocusField project! This guide covers how to set up your environment, the expected development workflow, and the structure of our prototyping workbench.

## 1. Environment Setup

We use **Pixi** to manage our dependencies and environment. This ensures that every developer has the exact same Python version, libraries, and system dependencies, eliminating "it works on my machine" issues.

### Prerequisites
- Install [Pixi](https://pixi.sh/).

### Installation
Clone the repository and run the following command in the project root:

```bash
pixi install
```

This will read the `pixi.toml` and `pixi.lock` files to create an isolated `.pixi` environment containing Python 3.11+, JupyterLab, and all required machine learning and NLP libraries (e.g., `scikit-learn`, `spacy`, `sentence-transformers`, `onnx`).

### Starting the Workbench
To start the JupyterLab environment and begin development, run:

```bash
pixi run jupyter lab
```

This will launch the prototyping interface where all of our iterative design and modeling takes place.

---

## 2. Project Architecture & Concepts

### The Goal: In-Browser Semantic Guardrails
Our objective is to create real-time feedback mechanisms for web textareas. Heavy LLM calls have too much latency (1-5 seconds) for character-by-character feedback. We are building "tiny models" (< 1MB) that can run in the browser (e.g., via ONNX or TensorFlow.js) with sub-100ms latency.

### The Three-Tier Detection Strategy
We structure our models to catch three types of issues:
1.  **Tier 1: Patterns (The Hard No's)**
    *   **Focus:** Hard rules (PHI, PII, specific blocked words).
    *   **Tools:** Optimized Regex, lightweight `spacy` NER.
2.  **Tier 2: Semantic Drift (The "Stay on Topic")**
    *   **Focus:** Ensuring the user's intent matches the required policy (e.g., a "Biography" doesn't become a "Product Review").
    *   **Tools:** Cosine similarity via Tiny Embeddings (e.g., `all-MiniLM-L6-v2`), Zero-Shot Classification.
3.  **Tier 3: Structural Completeness**
    *   **Focus:** Form, density, and length heuristics.
    *   **Tools:** Word counts, Part-of-Speech density analysis.

---

## 3. The Development Workflow

Our workflow is centered around the **"Policy Editor"** concept built in JupyterLab.

### Step 1: Define a Policy
A policy dictates what is expected and what is forbidden (e.g., "Topic: Person, No-Go: Medical Info").

### Step 2: Generate Synthetic Data ("The Seed")
Use larger LLMs (like GPT-4 or Llama-3 via `LiteLLM`/`Ollama`) to generate labeled datasets.
-   We create "Good" examples that adhere to the policy.
-   We create "Bad" examples that violate specific exclusion rules (e.g., introducing a social security number into a biography).
-   These datasets form our **"Intent Library"**.

### Step 3: Train a Tiny Model
Train a lightweight model (e.g., Random Forest, SVM, Logistic Regression on TF-IDF features) using the generated dataset.
-   We aim for high accuracy on the specific policy, heavily penalizing false positives for "Tier 1" violations.

### Step 4: Real-time Simulation
Use Jupyter Notebooks with `ipywidgets` to simulate a browser textarea.
-   **Requirement:** The model inference loop *must* execute in < 100ms to provide fluid visual feedback (Green/Yellow/Red indicators).

### Step 5: Export
Once validated in the notebook simulator, export the model to a format suitable for the browser (e.g., ONNX format).

---

## 4. Useful Commands

| Command | Description |
| :--- | :--- |
| `pixi install` | Installs or updates dependencies from `pixi.toml` |
| `pixi run jupyter lab` | Starts the Jupyter Lab server |
| `pixi add <package>` | Adds a new dependency to the project |

## 5. Directory Structure (Proposed)
*(To be created as development starts)*
-   `/notebooks/` - Jupyter notebooks containing the Policy Editor, UI simulation, and training pipelines.
-   `/data/` - Synthetically generated Intent Libraries (`.csv`, `.jsonl`).
-   `/models/` - Exported tiny models (e.g., `.onnx` files).
-   `/src/` - Reusable Python modules (data generation scripts, ONNX export utilities).
