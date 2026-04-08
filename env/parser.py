def parse_action(action_text: str):
    action_text = action_text.lower()

    if "s3" in action_text:
        return "fix_s3"

    elif "port" in action_text or "ssh" in action_text:
        return "fix_ec2"

    elif "iam" in action_text or "policy" in action_text:
        return "fix_iam"

    return "unknown"