def grade_action(action, expected):
    action = action.lower()

    if expected == "fix_s3" and "s3" in action:
        return 0.6

    elif expected == "fix_ec2" and ("port" in action or "ssh" in action):
        return 0.6

    elif expected == "fix_iam" and "iam" in action:
        return 0.6

    elif "verify" in action:
        return 0.95

    elif any(word in action for word in ["s3", "port", "iam"]):
        return 0.3

    return 0.05