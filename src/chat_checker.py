"""
Chat Checker for Vedaz Assignment

Validates:
- Chat structure
- Word count
- Duplicate detection
- Safety rules
- Train/Test split
"""

from rapidfuzz import fuzz

from utils import (
    load_jsonl,
    save_jsonl,
    write_report,
    split_dataset,
    count_words,
)


class ChatChecker:

    def __init__(self):
        self.unsafe_words = [
            "death",
            "die",
            "serious illness",
            "guaranteed",
            "100%",
            "ruined",
            "black magic",
            "pay money",
        ]

    def validate_structure(self, chat):
        """
        Check message order:
        system -> user -> assistant
        """

        messages = chat.get("messages", [])

        if len(messages) < 3:
            return False

        if messages[0]["role"] != "system":
            return False

        if messages[1]["role"] != "user":
            return False

        if messages[2]["role"] != "assistant":
            return False

        return True

    def safety_check(self, chat):

        text = " ".join(
            message["content"].lower()
            for message in chat["messages"]
        )

        violations = []

        for word in self.unsafe_words:
            if word in text:
                violations.append(word)

        return violations

    def duplicate_check(self, chats, threshold=90):

        duplicates = []

        for i in range(len(chats)):

            first = " ".join(
                msg["content"]
                for msg in chats[i]["messages"]
            )

            for j in range(i + 1, len(chats)):

                second = " ".join(
                    msg["content"]
                    for msg in chats[j]["messages"]
                )

                similarity = fuzz.ratio(first, second)

                if similarity >= threshold:
                    duplicates.append((i, j, similarity))

        return duplicates

    def analyze(self, input_file):

        chats = load_jsonl(input_file)

        valid = []
        invalid = []

        report = []

        total_words = 0

        for index, chat in enumerate(chats):

            structure = self.validate_structure(chat)

            if structure:
                valid.append(chat)
            else:
                invalid.append(chat)

            words = count_words(chat["messages"])

            total_words += words

            violations = self.safety_check(chat)

            report.append(
                f"""
Chat {index+1}

Structure : {"PASS" if structure else "FAIL"}

Words : {words}

Safety Violations : {violations if violations else "None"}

----------------------------------------
"""
            )

        duplicates = self.duplicate_check(valid)

        train, test = split_dataset(valid)

        save_jsonl(train, "data/train.jsonl")
        save_jsonl(test, "data/test.jsonl")

        final_report = f"""
VEDAZ CHAT CHECK REPORT

=============================

Total Chats : {len(chats)}

Valid Chats : {len(valid)}

Invalid Chats : {len(invalid)}

Average Words : {round(total_words/len(chats),2)}

Duplicate Chats : {len(duplicates)}

=============================

"""

        final_report += "\n".join(report)

        write_report(
            final_report,
            "reports/checker_report.txt",
        )

        print(final_report)

        return {
            "total": len(chats),
            "valid": len(valid),
            "invalid": len(invalid),
            "duplicates": duplicates,
        }


if __name__ == "__main__":

    checker = ChatChecker()

    checker.analyze(
        "data/vedaz_astrologer_finetune.jsonl"
    )