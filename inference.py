import os
import asyncio
from typing import List, Optional
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

MAX_STEPS = 5


def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


def build_smart_action(observation):
    resources = observation.get("resources", [])

    for r in resources:
        if r["type"] == "s3" and r["config"].get("public"):
            return "Fix public S3 bucket by making it private"

        if r["type"] == "ec2" and r["config"].get("open_port") == 22:
            return "Close port 22 to secure the instance"

        if r["type"] == "iam" and r["config"].get("policy") == "admin_access":
            return "Restrict IAM policy to least privilege"

    return "No issue detected"


async def main():
    from env.environment import CloudEnv

    env = CloudEnv()

    rewards = []
    steps_taken = 0

    log_start(task="cloud_security", env="cloud_env", model=MODEL_NAME)

    try:
        for level in ["easy", "medium", "hard"]:

            observation = env.reset(level)

            for step in range(1, MAX_STEPS + 1):

                obs_dict = observation.model_dump()

                action = build_smart_action(obs_dict)

                observation, reward, done, _ = env.step(action)

                rewards.append(reward)
                steps_taken += 1

                log_step(step, action, reward, done, None)

                if done:
                    break

        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = min(max(score, 0.0), 1.0)

        success = score > 0.5

    except Exception as e:
        log_step(steps_taken, "error", 0.0, True, str(e))
        success = False
        score = 0.0

    log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    asyncio.run(main())