def parse_action(action_text: str):
    action_text = action_text.lower()

    if "s3" in action_text:
        return "fix_s3"

    if "port" in action_text or "ssh" in action_text:
        return "fix_ec2"

    if "iam" in action_text:
        return "fix_iam"

    if "verify" in action_text:
        return "verify"

    return "unknown"