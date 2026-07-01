"""
Utility functions for the Vedaz AI Safety Pipeline.
Handles JSONL files, reports, dataset splitting, and word counting.
"""

import json
from pathlib import Path
from typing import List, Dict
from sklearn.model_selection import train_test_split


# ----------------------------
# JSONL Functions
# ----------------------------

def load_jsonl(file_path: str) -> List[Dict]:
    """Load chats from a JSONL file."""
    chats = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chats.append(json.loads(line))

    return chats


def save_jsonl(data: List[Dict], file_path: str):
    """Save chats to a JSONL file."""

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


# ----------------------------
# JSON Functions
# ----------------------------

def load_json(file_path: str):
    """Load a JSON file."""

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, file_path: str):
    """Save data as JSON."""

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ----------------------------
# Report Functions
# ----------------------------

def write_report(report: str, file_path: str):
    """Write report to text file."""

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report)


# ----------------------------
# Chat Utilities
# ----------------------------

def count_words(messages: List[Dict]) -> int:
    """Count total words in a chat."""

    total = 0

    for message in messages:
        total += len(message["content"].split())

    return total


# ----------------------------
# Dataset Split
# ----------------------------

def split_dataset(chats: List[Dict], test_size: float = 0.2):
    """Split dataset into train and test."""

    train, test = train_test_split(
        chats,
        test_size=test_size,
        random_state=42,
        shuffle=True
    )

    return train, test


# ----------------------------
# File Check
# ----------------------------

def ensure_directory(path: str):
    """Create directory if it does not exist."""

    Path(path).mkdir(parents=True, exist_ok=True)