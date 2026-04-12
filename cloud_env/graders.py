def clamp(score):
    return max(0.01, min(score, 0.99))


def grade_easy(observation=None, action=None, info=None):
    if observation is None:
        return 0.01  # ✅ fixed

    fixed = getattr(observation, "issues_found", [])
    verified = info.get("verified", False) if info else False

    if "s3" in fixed and verified:
        return clamp(0.9)
    elif "s3" in fixed:
        return clamp(0.5)
    else:
        return clamp(0.1)


def grade_medium(observation=None, action=None, info=None):
    if observation is None:
        return 0.01  # ✅ fixed

    fixed = getattr(observation, "issues_found", [])
    verified = info.get("verified", False) if info else False

    score = 0.0

    if "s3" in fixed:
        score += 0.3
    if "ec2" in fixed:
        score += 0.3

    if verified and score >= 0.6:
        score += 0.3

    return clamp(score)


def grade_hard(observation=None, action=None, info=None):
    if observation is None:
        return 0.01  # ✅ fixed

    fixed = getattr(observation, "issues_found", [])
    verified = info.get("verified", False) if info else False

    score = 0.0

    if "s3" in fixed:
        score += 0.25
    if "ec2" in fixed:
        score += 0.25
    if "iam" in fixed:
        score += 0.25

    if verified and score >= 0.75:
        score += 0.2

    return clamp(score)