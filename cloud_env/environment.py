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
            "level": level,
            "fixed": False,
            "verified": False,

            # 🔥 CRITICAL: grader attached from tasks.py
            "grader": task["grader"]
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

        action = action_text.lower()

        # 🔥 USE TASK-LEVEL GRADER
        grader_fn = self.state["grader"]
        reward = grader_fn(action)

        # 🔧 FIX PHASE
        if not self.state["fixed"]:
            if reward >= 0.6:
                self.state["fixed"] = True
                self.state["issues_found"].append("fixed")

        # 🔍 VERIFY PHASE
        elif self.state["fixed"] and not self.state["verified"]:
            if reward >= 0.95:
                self.state["verified"] = True

        done = self.state["verified"] or self.state["step_count"] >= 5

        observation = Observation(
            resources=self.state["resources"],
            issues_found=self.state["issues_found"],
            step_count=self.state["step_count"]
        )

        return observation, reward, done, {}

    def state(self):
        return self.state