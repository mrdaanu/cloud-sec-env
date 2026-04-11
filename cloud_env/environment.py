from cloud_env.parser import parse_action
from cloud_env.models import Observation, Resource
from cloud_env.tasks import load_task
import random


class CloudEnv:

    def __init__(self):
        self.state = None

    def reset(self, level="easy"):
        task = load_task(level)

        resources = [
            Resource(
                id=r["id"],
                type=r["type"],
                config=r["config"]
            )
            for r in task["resources"]
        ]

        # 🔥 Hidden IAM (safe randomness)
        hidden_iam = False
        if level in ["medium", "hard"]:
            if random.random() < 0.4:
                hidden_iam = True

        self.state = {
            "resources": resources,
            "issues_found": [],
            "step_count": 0,
            "verified": False,
            "level": level,
            "hidden_iam": hidden_iam,
            "verify_attempted": False
        }

        return Observation(
            resources=resources,
            issues_found=[],
            step_count=0
        )

    def step(self, action_text):

        if self.state is None:
            raise Exception("Call reset() first")

        self.state["step_count"] += 1
        action_text = action_text.lower()

        fixed = self.state["issues_found"]
        level = self.state["level"]

        required = {
            "easy": ["s3"],
            "medium": ["s3", "ec2"],
            "hard": ["s3", "ec2", "iam"]
        }

        needed = required[level].copy()

        # 🔥 hidden IAM logic
        if self.state.get("hidden_iam") and "iam" not in needed:
            needed.append("iam")

        reward = 0.06  # default penalty

        if not self.state["verified"]:

            # 🔧 FIX S3
            if "s3" not in fixed and "s3" in action_text:
                fixed.append("s3")
                reward = 0.56

            # 🔧 FIX EC2
            elif "ec2" not in fixed and ("port" in action_text or "ssh" in action_text):
                fixed.append("ec2")
                reward = 0.57

            # 🔧 FIX IAM
            elif "iam" not in fixed and "iam" in action_text:
                if level == "hard" or self.state.get("hidden_iam"):
                    fixed.append("iam")
                    reward = 0.59
                else:
                    reward = 0.06

            # 🔍 VERIFY
            elif "verify" in action_text:
                self.state["verify_attempted"] = True

                if all(issue in fixed for issue in needed):
                    self.state["verified"] = True
                    reward = 0.88
                else:
                    reward = 0.06

            else:
                reward = 0.05

        done = self.state["verified"] or self.state["step_count"] >= 6

        observation = Observation(
            resources=self.state["resources"],
            issues_found=fixed,
            step_count=self.state["step_count"]
        )

        return observation, reward, done, {}

    def state(self):
        return self.state