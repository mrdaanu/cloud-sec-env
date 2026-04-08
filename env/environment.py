from env.tasks import load_task
from env.models import Observation, Resource


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

        # Detect expected action
        resource_type = task["resources"][0]["type"]

        if resource_type == "s3":
            expected_action = "fix_s3"
        elif resource_type == "ec2":
            expected_action = "fix_ec2"
        elif resource_type == "iam":
            expected_action = "fix_iam"
        else:
            expected_action = "unknown"

        self.state = {
            "resources": resources,
            "issues_found": [],
            "step_count": 0,
            "expected_action": expected_action,
            "fixed": False,
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
        expected = self.state["expected_action"]

        reward = 0.05  # default small reward (never 0)

        # 🔧 FIX PHASE
        if not self.state["fixed"]:

            if expected == "fix_s3" and "s3" in action_text:
                self.state["fixed"] = True
                self.state["issues_found"].append("fixed")
                reward = 0.6

            elif expected == "fix_ec2" and ("port" in action_text or "ssh" in action_text):
                self.state["fixed"] = True
                self.state["issues_found"].append("fixed")
                reward = 0.6

            elif expected == "fix_iam" and "iam" in action_text:
                self.state["fixed"] = True
                self.state["issues_found"].append("fixed")
                reward = 0.6

            elif any(word in action_text for word in ["s3", "port", "iam"]):
                reward = 0.3  # partial progress

            else:
                reward = 0.05  # wrong but not zero/negative

        # 🔍 VERIFY PHASE
        elif self.state["fixed"] and not self.state["verified"]:

            if "verify" in action_text:
                self.state["verified"] = True
                reward = 0.95  # final success but < 1

            else:
                reward = 0.05

        done = self.state["verified"] or self.state["step_count"] >= 5

        observation = Observation(
            resources=self.state["resources"],
            issues_found=self.state["issues_found"],
            step_count=self.state["step_count"]
        )

        return observation, reward, done, {}

    def state(self):
        return self.state