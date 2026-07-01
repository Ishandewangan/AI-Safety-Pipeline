import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from prompts import CHAT_GENERATION_PROMPT
from utils import save_jsonl

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env file")

client = InferenceClient(token=HF_TOKEN)


# =========================
# CLEAN OUTPUT
# =========================
def clean_output(text: str):
    """Extract FIRST complete JSON object only."""
    if not text:
        return None
    
    text = text.replace("<|assistant|>", "")
    text = text.replace("<|user|>", "")
    text = text.replace("[/USER]", "")
    text = text.replace("[/ASSISTANT]", "")
    text = text.replace("[/VEDAZ]", "")
    text = text.replace("[/ASS]", "")

    # Find FIRST opening brace
    start = text.find("{")
    if start == -1:
        return None

    # Count braces to find matching closing brace
    brace_count = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            brace_count += 1
        elif text[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                return text[start:i + 1].strip()
    
    return None


# =========================
# STRICT JSON VALIDATION
# =========================
def parse_json(text: str):
    try:
        data = json.loads(text)

        # normalize schema (IMPORTANT FIX)
        if "message" in data:
            return {"message": data["message"]}

        if "assistant" in data and isinstance(data["assistant"], dict):
            if "message" in data["assistant"]:
                return {"message": data["assistant"]["message"]}
            if "response" in data["assistant"]:
                return {"message": data["assistant"]["response"]}

        return None

    except:
        return None


class ChatGenerator:

    def __init__(self):
        self.model = "HuggingFaceH4/zephyr-7b-beta"

        self.total = 0
        self.success = 0
        self.failed = 0

    # =========================
    # GENERATE SINGLE CHAT
    # =========================
    def generate_chat(self, topic):

        prompt = CHAT_GENERATION_PROMPT.format(topic=topic)

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Vedaz AI.\n"
                            "Return ONLY one valid JSON object.\n"
                            "No text before or after JSON.\n"
                            "No roles, no chat formatting.\n"
                            "Format strictly:\n"
                            "{ \"message\": \"...\" }"
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=400,
                temperature=0.1
            )

            raw = response.choices[0].message.content

            print("\n🟡 RAW OUTPUT:\n", raw)

            cleaned = clean_output(raw)

            data = parse_json(cleaned)

            if data:
                print("🟢 SUCCESS JSON PARSED")
                self.success += 1
                return data

            print("🔴 FAILED JSON")
            print(cleaned)
            self.failed += 1
            return None

        except Exception as e:
            print(f"❌ API ERROR: {e}")
            self.failed += 1
            return None

    # =========================
    # GENERATE MULTIPLE
    # =========================
    def generate_multiple(self, topics, output_file):

        results = []

        for i, topic in enumerate(topics, 1):
            self.total += 1

            print(f"\n==============================")
            print(f"Generating {i}/{len(topics)}: {topic}")
            print(f"==============================")

            chat = self.generate_chat(topic)

            if chat:
                results.append(chat)
            else:
                print("⚠️ Skipped")

        save_jsonl(results, output_file)

        print("\n==============================")
        print("📊 FINAL REPORT")
        print("==============================")
        print(f"Total:   {self.total}")
        print(f"Success: {self.success}")
        print(f"Failed:  {self.failed}")
        print(f"Saved:   {len(results)}")
        print("==============================")

        return results


if __name__ == "__main__":

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
        "Spiritual growth"
    ]

    ChatGenerator().generate_multiple(
        topics,
        "data/generated_chats.jsonl"
    )