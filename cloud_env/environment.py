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

        expected = []
        for r in task["resources"]:
            if r["type"] == "s3":
                expected.append("s3")
            elif r["type"] == "ec2":
                expected.append("ec2")
            elif r["type"] == "iam":
                expected.append("iam")

        self.state = {
            "resources": resources,
            "issues_found": [],
            "expected": expected,
            "fixed": [],
            "step_count": 0,
            "verified": False,
            "history": []
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

        step = self.state["step_count"]

        
        reward = max(0.05, 0.1 - (step * 0.005))

        #  anti-loop
        if action_text in self.state["history"]:
            reward = 0.05

        self.state["history"].append(action_text)

        
        for issue in self.state["expected"]:
            if issue not in self.state["fixed"]:

                if issue == "s3" and "s3" in action_text:
                    self.state["fixed"].append("s3")
                    reward = 0.5 - (step * 0.01)

                elif issue == "ec2" and ("port" in action_text or "ssh" in action_text):
                    self.state["fixed"].append("ec2")
                    reward = 0.5 - (step * 0.01)

                elif issue == "iam" and "iam" in action_text:
                    self.state["fixed"].append("iam")
                    reward = 0.5 - (step * 0.01)

                elif any(k in action_text for k in ["s3", "port", "iam"]):
                    reward = 0.2

                else:
                    reward = 0.05

                break

        #  HIDDEN  (ONLY HARD)
        if len(self.state["expected"]) >= 3:
            if "s3" in self.state["fixed"] and "iam" not in self.state["expected"]:
                if "iam" not in self.state["fixed"] and step == 2:
                    self.state["expected"].append("iam")

        #  VERIFY PHASE
        if set(self.state["fixed"]) == set(self.state["expected"]):
            if "verify" in action_text:
                reward = 0.9 - (step * 0.01)
                reward = max(0.6, reward)  # keep strong reward
                self.state["verified"] = True

        done = self.state["verified"] or step >= 6

        observation = Observation(
            resources=self.state["resources"],
            issues_found=self.state["fixed"],
            step_count=step
        )

        return observation, reward, done, {}

    def state(self):
        return self.state