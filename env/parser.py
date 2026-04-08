def parse_action(text: str):
    text = text.lower()

    # S3 detection
    if "s3" in text or "bucket" in text or "public" in text:
        return "fix_s3_public"

    # EC2 detection
    elif "port" in text or "ssh" in text:
        return "close_port"

    # IAM detection
    elif "iam" in text or "policy" in text or "permission" in text:
        return "fix_iam"

    return "unknown"