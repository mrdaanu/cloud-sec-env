from env.parser import parse_action
from env.graders import grade_action
from env.tasks import load_task
from env.models import Observation, Resource


class CloudEnv:

    def __init__(self):
        self.state = None

    def reset(self, level="easy"):
        task = load_task(level)

        # ✅ Create resources
        resources = [
            Resource(
                id=r["id"],
                type=r["type"],
                config=r["config"]
            )
            for r in task["resources"]
        ]

        # ✅ FIX: detect expected action OUTSIDE dict
        resource_type = task["resources"][0]["type"]

        if resource_type == "s3":
            expected_action = "fix_s3"
        elif resource_type == "ec2":
            expected_action = "fix_ec2"
        elif resource_type == "iam":
            expected_action = "fix_iam"
        else:
            expected_action = "unknown"

        # ✅ Proper state dictionary
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

        action = parse_action(action_text)
        expected = self.state["expected_action"]

        reward = 0.0

        # 🔧 FIX PHASE
        if not self.state["fixed"]:
            if action == expected:
                self.state["fixed"] = True
                self.state["issues_found"].append("fixed")
                reward = 0.7
            elif action != "unknown":
                reward = 0.3
            else:
                reward = -0.1

        # 🔍 VERIFY PHASE
        elif self.state["fixed"] and not self.state["verified"]:
            if "verify" in action_text.lower():
                self.state["verified"] = True
                reward = 1.0
            else:
                reward = -0.1

        done = self.state["verified"] or self.state["step_count"] >= 5

        observation = Observation(
            resources=self.state["resources"],
            issues_found=self.state["issues_found"],
            step_count=self.state["step_count"]
        )

        return observation, reward, done, {}

    def state(self):
        return self.state