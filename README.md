# IntentGate / FocusField: Lite-NLP Browser Feedback Workbench

## Overview
This project is a Jupyter-based prototyping environment designed to build, test, and evaluate non-LLM, real-time NLP feedback mechanisms for web-based textareas. The ultimate goal is to create lightweight semantic guardrails ("Intent Compliance") that can execute entirely within a user's browser (e.g., via ONNX or TensorFlow.js) with sub-100ms latency.

Rather than relying on heavy, slow LLM API calls for every keystroke, this workbench helps you train "tiny models" and build heuristic pipelines to detect:
1.  **Pattern Violations (The Hard No's):** e.g., PII/PHI leakage.
2.  **Semantic Drift:** e.g., Is the user staying on the requested topic?
3.  **Structural Completeness:** e.g., Is the response substantive?

## Features
-   **Synthetic Data Generation:** Tools to use larger LLMs to generate labeled "good" and "bad" text samples (the "Intent Library").
-   **Policy Editor Workflow:** A streamlined process to define a policy, generate training data, train a tiny SVM/Random Forest model, and export it.
-   **Real-time UI Prototyping:** Jupyter Notebook interfaces utilizing `ipywidgets` to simulate a browser textarea and visualize real-time classification feedback.
-   **Deterministic Environment:** Managed entirely by Pixi, ensuring absolute reproducibility across developer machines.

## Getting Started
To get the project running on your local machine, please see the onboarding guide in [develop.md](develop.md).

## Project Documentation
-   [Requirements Document](requirements.md) - Detailed technical specifications and functional requirements.
-   [Developer Guide](develop.md) - Setup instructions, architectural decisions, and contribution guidelines.