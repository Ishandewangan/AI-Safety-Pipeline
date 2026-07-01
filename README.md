# AI Safety Pipeline

This repository contains a small AI safety pipeline for processing astrology-related chat data. It performs three main steps:

1. Checks chat structure, word count, duplicate content, and basic safety violations.
2. Generates new chat examples from selected topics.
3. Evaluates sample responses using a simple rule-based quality checker.

## Project Structure

- `main.py` — entry point that runs the full pipeline.
- `src/chat_checker.py` — validates input chat data and writes a checker report.
- `src/chat_generator.py` — generates chat outputs using a Hugging Face model.
- `src/quality_tester.py` — scores sample responses for safety, helpfulness, honesty, and tone.
- `data/` — training, test, and generated chat datasets.
- `reports/` — output reports and evaluation results.

## Requirements

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Setup

Create and activate a virtual environment if needed:

```bash
python -m venv venv
venv\Scripts\activate
```

Create a `.env` file in the project root and add your Hugging Face token:

```env
HF_TOKEN=your_huggingface_token_here
```

## Run the Pipeline

Execute the main script:

```bash
python main.py
```

This will generate or update:

- `data/train.jsonl`
- `data/test.jsonl`
- `data/generated_chats.jsonl`
- `reports/checker_report.txt`
- `reports/evaluation_results.csv`

## Notes

- The chat generator depends on the Hugging Face Inference API and requires a valid `HF_TOKEN`.
- The quality tester is currently rule-based and intended for lightweight evaluation rather than full LLM-based scoring.
