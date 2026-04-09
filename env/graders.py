def grade_easy(action: str) -> float:
    action = action.lower()

    if "s3" in action and "private" in action:
        return 0.9   # ✅ not 1.0
    elif "s3" in action:
        return 0.5
    else:
        return 0.1


def grade_medium(action: str) -> float:
    action = action.lower()

    if "port" in action or "ssh" in action:
        return 0.9
    elif "port" in action:
        return 0.5
    else:
        return 0.1


def grade_hard(action: str) -> float:
    action = action.lower()

    if "iam" in action or "policy" in action:
        return 0.9
    elif "iam" in action:
        return 0.5
    else:
        return 0.1