from env.parser import parse_action
from env.graders import grade_action
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

        self.state = {
            "resources": resources,
            "issues_found": [],
            "step_count": 0,
            "expected_actions": task["expected_actions"]
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
        expected_actions = self.state["expected_actions"]

        reward = 0.0

        # ✅ reward for correct new fix
        if action in expected_actions:
            reward = 1.0
            expected_actions.remove(action)
            self.state["issues_found"].append(action)

        # ⚠️ partial correct
        elif action != "unknown":
            reward = 0.3

        # ❌ wrong
        else:
            reward = -0.1

        done = len(expected_actions) == 0 or self.state["step_count"] >= 6

        observation = Observation(
            resources=self.state["resources"],
            issues_found=self.state["issues_found"],
            step_count=self.state["step_count"]
        )

        return observation, reward, done, {}