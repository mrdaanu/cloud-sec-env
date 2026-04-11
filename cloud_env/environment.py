from cloud_env.parser import parse_action
import random
from cloud_env.models import Observation, Resource
from cloud_env.tasks import load_task


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

        # expected issues list
        expected_issues = []
        for r in task["resources"]:
            if r["type"] == "s3":
                expected_issues.append("s3")
            elif r["type"] == "ec2":
                expected_issues.append("ec2")
            elif r["type"] == "iam":
                expected_issues.append("iam")

        self.state = {
            "resources": resources,
            "issues_found": [],
            "step_count": 0,
            "expected_issues": expected_issues,
            "fixed": [],
            "verified": False
        }

        return Observation(
            resources=resources,
            issues_found=[],
            step_count=0
        )

    def step(self, action_text):

        if self.state is None:
            raise Exception("Call reset first")

        self.state["step_count"] += 1
        action_text = action_text.lower()

        reward = 0.05  # base small reward (SAFE > 0)

        # ===== FIX PHASE =====
        for issue in self.state["expected_issues"]:

            if issue not in self.state["fixed"]:

                if issue == "s3" and "s3" in action_text:
                    self.state["fixed"].append("s3")
                    reward = 0.4

                elif issue == "ec2" and ("port" in action_text or "ssh" in action_text):
                    self.state["fixed"].append("ec2")
                    reward = 0.4

                elif issue == "iam" and "iam" in action_text:
                    self.state["fixed"].append("iam")
                    reward = 0.4

                elif any(word in action_text for word in ["s3", "port", "iam"]):
                    reward = 0.2  # partial relevance

                else:
                    reward = 0.05

                break

        # ===== VERIFY PHASE =====
        if len(self.state["fixed"]) == len(self.state["expected_issues"]):
            if "verify" in action_text:
                self.state["verified"] = True
                reward = 0.9

        done = self.state["verified"] or self.state["step_count"] >= 6

        observation = Observation(
            resources=self.state["resources"],
            issues_found=self.state["fixed"],
            step_count=self.state["step_count"]
        )

        return observation, reward, done, {}

    def state(self):
        return self.state