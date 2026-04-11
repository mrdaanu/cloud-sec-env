def grade_easy(observation=None, action=None, info=None):
    if observation is None:
        return 0.0

    fixed = getattr(observation, "issues_found", [])
    verified = info.get("verified", False) if info else False

    if "s3" in fixed and verified:
        return 0.9
    elif "s3" in fixed:
        return 0.5
    else:
        return 0.1


def grade_medium(observation=None, action=None, info=None):
    if observation is None:
        return 0.0

    fixed = getattr(observation, "issues_found", [])
    verified = info.get("verified", False) if info else False

    score = 0.0

    if "s3" in fixed:
        score += 0.3
    if "ec2" in fixed:
        score += 0.3

    if verified and score >= 0.6:
        score += 0.3

    return min(score, 0.95)


def grade_hard(observation=None, action=None, info=None):
    if observation is None:
        return 0.0

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

    return min(score, 0.95)