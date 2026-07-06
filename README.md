# AI Safety Pipeline

This project demonstrates an AI Safety Pipeline for a Vedic Astrology chatbot. It validates conversation datasets, generates new user chat messages using the Hugging Face Zephyr-7B model, and evaluates response quality using rule-based scoring.

---

## Features

- Validate AI conversation datasets
- Check chat structure
- Detect unsafe content
- Detect duplicate conversations
- Split dataset into training and testing data
- Generate new user chat messages using Hugging Face
- Evaluate AI response quality
- Generate reports automatically

---

## Workflow

```text
                    main.py
                       │
                       ▼
     Load Dataset (vedaz_astrologer_finetune.jsonl)
                       │
                       ▼
                 ChatChecker
        ├─ Validate chat structure
        ├─ Count words
        ├─ Check unsafe content
        ├─ Detect duplicate chats
        └─ Split dataset into Train/Test
                       │
                       ▼
         train.jsonl & test.jsonl
                       │
                       ▼
                ChatGenerator
        ├─ Create prompt
        ├─ Send prompt to Hugging Face (Zephyr-7B)
        ├─ Generate new user chat messages
        ├─ Clean AI output
        ├─ Validate JSON
        └─ Save generated_chats.jsonl
                       │
                       ▼
               QualityTester
        ├─ Safety Score
        ├─ Helpfulness Score
        ├─ Honesty Score
        ├─ Tone Score
        ├─ Calculate Overall Score
        └─ Save evaluation_results.csv
```

---

## Project Structure

```
AI-Safety-Pipeline/
│
├── data/
│   ├── vedaz_astrologer_finetune.jsonl
│   ├── train.jsonl
│   ├── test.jsonl
│   └── generated_chats.jsonl
│
├── reports/
│   ├── checker_report.txt
│   └── evaluation_results.csv
│
├── src/
│   ├── chat_checker.py
│   ├── chat_generator.py
│   ├── quality_tester.py
│   ├── prompts.py
│   └── utils.py
│
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

## Modules

### ChatChecker

- Validates chat structure
- Counts total words
- Detects duplicate chats
- Checks for unsafe content
- Splits dataset into training and testing data
- Generates a checker report

---

### ChatGenerator

- Uses the Hugging Face Zephyr-7B model
- Generates new user chat messages from predefined topics
- Cleans AI output
- Validates JSON format
- Saves generated messages to `generated_chats.jsonl`

---

### QualityTester

Evaluates AI responses using simple rule-based scoring.

Scores:

- Safety
- Helpfulness
- Honesty
- Tone

Calculates an overall score and saves the results to:

```
reports/evaluation_results.csv
```

---

## Technologies Used

- Python
- Hugging Face Inference API
- Zephyr-7B Beta
- RapidFuzz
- Scikit-learn
- JSON / JSONL
- dotenv

---

## Installation

Install the required packages.

```bash
pip install -r requirements.txt
```

---

## Setup

Create a `.env` file.

```env
HF_TOKEN=your_huggingface_token
```

---

## Run the Project

```bash
python main.py
```

---

## Output Files

After running the pipeline, the following files are created.

```
data/train.jsonl
data/test.jsonl
data/generated_chats.jsonl

reports/checker_report.txt
reports/evaluation_results.csv
```

---

## Purpose

This project demonstrates a simple AI safety pipeline by:

- Validating conversation datasets
- Generating new user chat messages using AI
- Evaluating AI response quality
- Creating reports for analysis

It is designed as a beginner-friendly project to demonstrate AI safety concepts, data validation, prompt engineering, dataset preparation, and response evaluation.

---

## Future Improvements

- Generate complete conversations instead of only user messages
- Replace rule-based evaluation with LLM-based evaluation
- Add toxicity and hallucination detection
- Support multiple AI models
- Build a web interface using Streamlit or Flask

---

## Author

**Ishan Dewangan**