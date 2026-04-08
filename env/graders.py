def grade_action(action, expected):
    if action == expected:
        return 1.0

    elif action != "unknown":
        return 0.5

    return 0.0
    # EASY: S3 bucket
    if expected == "fix_s3":
        if "s3" in action and "private" in action:
            return 1.0
        elif "s3" in action:
            return 0.5
        else:
            return 0.0

    # MEDIUM: EC2 port
    elif expected == "fix_ec2":
        if "port" in action and "22" in action and "close" in action:
            return 1.0
        elif "port" in action:
            return 0.5
        else:
            return 0.0

    # HARD: IAM policy
    elif expected == "fix_iam":
        if "iam" in action and "least privilege" in action:
            return 1.0
        elif "iam" in action:
            return 0.5
        else:
            return 0.0

    return 0.0