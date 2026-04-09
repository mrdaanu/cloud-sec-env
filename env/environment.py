from env.tasks import load_task
from env.models import Observation, Resource
from env.graders import grade_easy, grade_medium, grade_hard


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
            "level": level,          # ✅ important for grader mapping
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

        action = action_text.lower()
        level = self.state["level"]

        # ✅ EXPLICIT GRADER MAPPING (CRITICAL FIX)
        if level == "easy":
            reward = grade_easy(action)
        elif level == "medium":
            reward = grade_medium(action)
        elif level == "hard":
            reward = grade_hard(action)
        else:
            reward = 0.05  # fallback safe reward

        # 🔧 FIX PHASE tracking
        if not self.state["fixed"]:
            if reward >= 0.6:
                self.state["fixed"] = True
                self.state["issues_found"].append("fixed")

        # 🔍 VERIFY PHASE tracking
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