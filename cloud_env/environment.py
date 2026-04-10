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

        # 🔥 Hidden issue logic (only for medium & hard)
        hidden_issue = None
        if level in ["medium", "hard"] and len(resources) > 1:
            hidden_issue = random.choice(resources).id

        self.state = {
            "resources": resources,
            "issues_found": [],
            "step_count": 0,
            "verified": False,
            "hidden_issue": hidden_issue,
            "revealed": False
        }

        # 🔍 Only show visible resources initially
        visible_resources = [
            r for r in resources if r.id != hidden_issue
        ]

        return Observation(
            resources=visible_resources,
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

        # 🔧 FIX LOGIC (MULTI-RESOURCE)
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

        # ❌ WRONG ACTION
        if not fixed_now and "verify" not in action_text:
            reward = -0.1

        # 🔥 REVEAL HIDDEN ISSUE AFTER FIRST FIX
        if (
            self.state["hidden_issue"]
            and not self.state["revealed"]
            and len(self.state["issues_found"]) >= 1
        ):
            self.state["revealed"] = True

        # 🔍 BUILD VISIBLE RESOURCES
        visible_resources = []

        for r in self.state["resources"]:
            if r.id == self.state["hidden_issue"] and not self.state["revealed"]:
                continue
            visible_resources.append(r)

        # 🔍 VERIFY ONLY AFTER ALL FIXED
        all_fixed = len(self.state["issues_found"]) == len(self.state["resources"])

        if all_fixed and "verify" in action_text:
            reward = 0.9
            self.state["verified"] = True

        done = self.state["verified"] or self.state["step_count"] >= 6

        observation = Observation(
            resources=visible_resources,
            issues_found=self.state["issues_found"],
            step_count=self.state["step_count"]
        )

        return observation, reward, done, {}

    def state(self):
        return self.state