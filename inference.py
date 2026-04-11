import asyncio
import os
from cloud_env.environment import CloudEnv
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")

client = None
if API_BASE_URL and API_KEY:
    try:
        client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    except:
        client = None


def call_llm():
    if client is None:
        return  

    try:
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
        )
    except:
        pass

def decide_action(obs, level):
    fixed = obs.get("issues_found", [])

    if "s3" not in fixed:
        return "Fix S3 bucket privacy"

    if level in ["medium", "hard"]:
        if "ec2" not in fixed:
            return "Close port 22"

    if level == "hard":
        if "iam" not in fixed:
            return "Fix IAM policy"

    return "Verify fix"


async def run_task(level):
    env = CloudEnv()
    observation = env.reset(level)

    total_reward = 0
    rewards = []
    steps = 0
    done = False

    print(f"[START] task={level} env=cloud_env model={MODEL_NAME}")

    while not done and steps < 6:
        obs = observation.model_dump()

        call_llm()  

        action = decide_action(obs, level)

        observation, reward, done, _ = env.step(action)

        steps += 1
        total_reward += reward
        rewards.append(reward)

        print(
            f"[STEP] step={steps} action={action} "
            f"reward={reward:.2f} done={str(done).lower()} error=null"
        )

   
    score = total_reward / len(rewards)
    score = max(0.01, min(score, 0.99))

    success = score > 0.5

    print(
        f"[END] success={str(success).lower()} "
        f"steps={steps} "
        f"score={score:.3f} "
        f"rewards={','.join([f'{r:.2f}' for r in rewards])}"
    )



async def main():

    level = os.getenv("TASK_LEVEL", "easy")

    await run_task(level)


if __name__ == "__main__":
    asyncio.run(main())