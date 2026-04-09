def grade_easy(action):
    action = action.lower()
    if "s3" in action:
        return 0.6
    elif "verify" in action:
        return 0.95
    elif "s3" in action:
        return 0.3
    return 0.05


def grade_medium(action):
    action = action.lower()
    if "port" in action or "ssh" in action:
        return 0.6
    elif "verify" in action:
        return 0.95
    elif "port" in action:
        return 0.3
    return 0.05


def grade_hard(action):
    action = action.lower()
    if "iam" in action:
        return 0.6
    elif "verify" in action:
        return 0.95
    elif "iam" in action:
        return 0.3
    return 0.05