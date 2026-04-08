import json


def load_task(level):

    if level == "easy":
        return {
            "resources": [
                {"id": "s3_1", "type": "s3", "config": {"public": True}},
                {"id": "ec2_1", "type": "ec2", "config": {"port_22_open": True}}
            ],
            "expected_actions": ["fix_s3", "fix_ec2"]
        }

    elif level == "medium":
        return {
            "resources": [
                {"id": "ec2_1", "type": "ec2", "config": {"port_22_open": True}},
                {"id": "iam_1", "type": "iam", "config": {"admin_access": True}}
            ],
            "expected_actions": ["fix_ec2", "fix_iam"]
        }

    elif level == "hard":
        return {
            "resources": [
                {"id": "s3_1", "type": "s3", "config": {"public": True}},
                {"id": "ec2_1", "type": "ec2", "config": {"port_22_open": True}},
                {"id": "iam_1", "type": "iam", "config": {"admin_access": True}}
            ],
            "expected_actions": ["fix_s3", "fix_ec2", "fix_iam"]
        }