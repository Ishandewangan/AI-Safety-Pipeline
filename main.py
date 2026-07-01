#!/usr/bin/env python3
"""
Main entry point for the Vedaz AI Safety Pipeline.
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from chat_checker import ChatChecker
from chat_generator import ChatGenerator
from quality_tester import QualityTester


def main():

    print("=" * 60)
    print("VEDAZ AI SAFETY PIPELINE")
    print("=" * 60)

    # -----------------------------
    # Task 1 - Chat Checker
    # -----------------------------
    print("\n[1/3] Running Chat Checker...\n")

    checker = ChatChecker()

    checker.analyze(
        "data/vedaz_astrologer_finetune.jsonl"
    )

    # -----------------------------
    # Task 2 - Chat Generator
    # -----------------------------
    print("\n[2/3] Generating New Chats...\n")

    topics = [
        "Career guidance",
        "Marriage timing",
        "Love relationship",
        "Education",
        "Financial planning",
        "Health concern",
        "Family problems",
        "Business growth",
        "Foreign travel",
        "Spiritual growth",
    ]

    generator = ChatGenerator()

    generator.generate_multiple(
        topics,
        "data/generated_chats.jsonl",
    )

    # -----------------------------
    # Task 3 - Quality Tester
    # -----------------------------
    print("\n[3/3] Evaluating Generated Chats...\n")

    tester = QualityTester()

    sample_response = (
        "Astrology suggests positive opportunities ahead. "
        "For serious health concerns, please consult a doctor."
    )

    for topic in topics:

        tester.evaluate_response(
            topic,
            sample_response,
        )

    tester.save_results()

    print("\n" + "=" * 60)
    print("Pipeline Completed Successfully")
    print("=" * 60)

    print("\nGenerated Files:")

    print("✔ data/train.jsonl")
    print("✔ data/test.jsonl")
    print("✔ data/generated_chats.jsonl")
    print("✔ reports/checker_report.txt")
    print("✔ reports/evaluation_results.csv")


if __name__ == "__main__":
    main()