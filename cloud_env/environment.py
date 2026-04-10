from cloud_env.parser import parse_action
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
            "verified": False
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
        fixed_now = False

        # 🔧 MULTI-RESOURCE FIX LOGIC
        for r in self.state["resources"]:

            if r.id in self.state["issues_found"]:
                continue

            if r.type == "s3" and "s3" in action_text:
                self.state["issues_found"].append(r.id)
                reward += 0.3
                fixed_now = True

            elif r.type == "ec2" and ("port" in action_text or "ssh" in action_text):
                self.state["issues_found"].append(r.id)
                reward += 0.3
                fixed_now = True

            elif r.type == "iam" and "iam" in action_text:
                self.state["issues_found"].append(r.id)
                reward += 0.3
                fixed_now = True

        if not fixed_now and "verify" not in action_text:
            reward = -0.1

        all_fixed = len(self.state["issues_found"]) == len(self.state["resources"])

        if all_fixed and "verify" in action_text:
            reward = 0.9
            self.state["verified"] = True

        done = self.state["verified"] or self.state["step_count"] >= 6

        observation = Observation(
            resources=self.state["resources"],
            issues_found=self.state["issues_found"],
            step_count=self.state["step_count"]
        )

        return observation, reward, done, {}

    def state(self):
        return self.state