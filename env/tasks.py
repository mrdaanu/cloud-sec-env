import json
import os


def load_task(level: str):
    """
    Loads a task based on difficulty level (easy, medium, hard)

    Ensures:
    - task structure is valid
    - required fields exist (expected_action, grader)
    """

    file_path = os.path.join("data", f"{level}.json")

    if not os.path.exists(file_path):
        raise Exception(f"Task file not found: {file_path}")

    with open(file_path, "r") as f:
        task = json.load(f)

    # ✅ REQUIRED FIELDS (validator expects this)
    required_fields = ["resources", "expected_action", "grader"]

    for field in required_fields:
        if field not in task:
            raise Exception(f"Task missing required field: {field}")

    # ✅ Ensure at least 1 resource exists
    if not isinstance(task["resources"], list) or len(task["resources"]) == 0:
        raise Exception("Task must contain at least one resource")

    # ✅ Normalize structure (safe for validator)
    task["task_id"] = task.get("task_id", level)
    task["difficulty"] = level

    return task