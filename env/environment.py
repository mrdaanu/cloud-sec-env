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
            "expected_action": task["expected_action"]
        }

        return Observation(
            resources=resources,
            issues_found=[],
            step_count=0
        )

    def step(self, action_text):
        self.state["step_count"] += 1

        action = parse_action(action_text)
        expected = self.state["expected_action"]

        reward = grade_action(action, expected)

        if reward == 1.0:
            self.state["issues_found"].append("fixed")

        done = reward == 1.0 or self.state["step_count"] > 5

        observation = Observation(
            resources=self.state["resources"],
            issues_found=self.state["issues_found"],
            step_count=self.state["step_count"]
        )

        return observation, reward, done, {}