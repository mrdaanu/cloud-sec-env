def load_task(level="easy"):

    if level == "easy":
        return {
            "resources": [
                {"id": "s3_1", "type": "s3", "config": {"public": True}}
            ],
            "expected_action": "fix_s3"
        }

    elif level == "medium":
        return {
            "resources": [
                {"id": "ec2_1", "type": "ec2", "config": {"port_22_open": True}}
            ],
            "expected_action": "fix_ec2"
        }

    elif level == "hard":
        return {
            "resources": [
                {"id": "iam_1", "type": "iam", "config": {"admin_access": True}}
            ],
            "expected_action": "fix_iam"
        }