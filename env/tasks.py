import json
import os
from env.graders import grade_easy, grade_medium, grade_hard


# 🔥 REGISTER GRADERS (THIS IS THE KEY FIX)
GRADER_MAP = {
    "easy": grade_easy,
    "medium": grade_medium,
    "hard": grade_hard
}


def load_task(level: str):
    file_path = os.path.join("data", f"{level}.json")

    if not os.path.exists(file_path):
        raise Exception(f"Task file not found: {file_path}")

    with open(file_path, "r") as f:
        task = json.load(f)

    # REQUIRED FIELDS
    required_fields = ["resources", "expected_action", "grader"]
    for field in required_fields:
        if field not in task:
            raise Exception(f"Task missing required field: {field}")

    # 🔥 ATTACH ACTUAL GRADER FUNCTION
    task["grader_fn"] = GRADER_MAP.get(level)

    if task["grader_fn"] is None:
        raise Exception(f"No grader found for level: {level}")

    return task