import json
import os
from env.graders import grade_easy, grade_medium, grade_hard


def load_task(level: str):

    file_path = os.path.join("data", f"{level}.json")

    if not os.path.exists(file_path):
        raise Exception(f"Task file not found: {file_path}")

    with open(file_path, "r") as f:
        task = json.load(f)

    # 🔥 ATTACH GRADER DIRECTLY TO TASK
    if level == "easy":
        task["grader"] = grade_easy

    elif level == "medium":
        task["grader"] = grade_medium

    elif level == "hard":
        task["grader"] = grade_hard

    else:
        raise Exception("Invalid task level")

    return task