# Lesson 05 – Advanced Prompt Engineering (Ollama)

This folder contains my solution for **Lesson 05 (Advanced Prompt Engineering)** from Microsoft’s *Generative AI for Beginners* course.

Instead of using a paid cloud API, I implemented the exercise using a **local LLM with Ollama**.

## What I built

- A small Flask app (`original_app.py`) as the “starting point”
- A local prompt-based reviewer (`review_with_ollama.py`) that:
  - sends the original code to Ollama
  - asks the model to critique and improve it
  - saves the improved version to `improved_app.py`

## Why this is “Advanced Prompt Engineering”

This exercise demonstrates:
- **Structured prompting** (clear rules, clear output format)
- **Reliability improvements** for small models
- **Iteration & robustness**:
  - The script first tries to parse strict JSON
  - If the model returns plain text + a code block, the script extracts the Python code and still succeeds

This matches real-world prompt engineering where models don’t always follow instructions perfectly.

## Requirements

- Python 3.x
- Ollama installed and running
- Model: `phi3:mini`

Install Python packages:

```bash
pip install flask requests