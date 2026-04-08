def load_task(level):
    if level == "easy":
        return {
            "resources": [
                {"id": "s3_1", "type": "s3", "config": {"public": True}}
            ],
            "expected_action": "fix_s3_public"
        }

    elif level == "medium":
        return {
            "resources": [
                {"id": "ec2_1", "type": "ec2", "config": {"open_port": 22}}
            ],
            "expected_action": "close_port"
        }

    elif level == "hard":
        return {
            "resources": [
                {"id": "iam_1", "type": "iam", "config": {"policy": "admin_access"}}
            ],
            "expected_action": "fix_iam"
        }