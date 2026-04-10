from cloud_env.parser import parse_action
import random
from cloud_env.tasks import load_task
from cloud_env.models import Observation, Resource


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

        self.state = {
            "resources": resources,
            "issues_found": [],
            "step_count": 0,
            "fixed": False,
            "verified": False,
            "history": [],
            "level": level,
            "hidden_issue": False
        }

        return Observation(
            resources=resources,
            issues_found=[],
            step_count=0
        )

    def step(self, action_text):

        if self.state is None:
            raise Exception("Call /reset before /step")

        self.state["step_count"] += 1
        action_text = action_text.lower()

        reward = 0.0

        
        if action_text in self.state["history"]:
            reward = -0.2
        else:
            self.state["history"].append(action_text)

        if not self.state["fixed"]:

            if "s3" in action_text:
                self.state["fixed"] = True
                self.state["issues_found"].append("s3_fixed")
                reward = 0.8

                
                if self.state["level"] != "easy":
                    self.state["hidden_issue"] = True

            elif "port" in action_text or "ssh" in action_text:
                self.state["fixed"] = True
                self.state["issues_found"].append("ec2_fixed")
                reward = 0.7

            elif "iam" in action_text:
                self.state["fixed"] = True
                self.state["issues_found"].append("iam_fixed")
                reward = 0.7

            elif any(word in action_text for word in ["s3", "port", "iam"]):
                reward = 0.3
            else:
                reward = -0.1

        elif self.state["hidden_issue"] and not self.state["verified"]:

            if "iam" in action_text:
                self.state["issues_found"].append("hidden_fixed")
                self.state["hidden_issue"] = False
                reward = 0.6
            else:
                reward = -0.1

        elif self.state["fixed"] and not self.state["verified"]:

            if "verify" in action_text:
                self.state["verified"] = True
                reward = 0.9
            else:
                reward = -0.1

        done = self.state["verified"] or self.state["step_count"] >= 6

        observation = Observation(
            resources=self.state["resources"],
            issues_found=self.state["issues_found"],
            step_count=self.state["step_count"]
        )

        return observation, reward, done, {}

    def state(self):
        return self.state