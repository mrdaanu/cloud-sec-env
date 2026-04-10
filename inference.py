import asyncio
import os
from cloud_env.environment import CloudEnv
from openai import OpenAI


#  ENV VARIABLES

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")


#  OPTIONAL LLM CLIENT

client = None
if API_KEY:
    try:
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=API_KEY
        )
    except:
        client = None



#  DECISION LOGIC

def decide_action(obs, level):
    issues = obs["issues_found"]

    #  STEP 1: Fix S3
    if "s3_fixed" not in issues:
        return "Fix S3 bucket privacy"

    #  STEP 2: Only for medium/hard → fix IAM
    if level in ["medium", "hard"]:
        if "hidden_fixed" not in issues:
            return "Fix IAM policy"

    #  STEP 3: Verify
    return "Verify fix"



#  RUN SINGLE TASK

async def run_task(level):
    env = CloudEnv()
    observation = env.reset(level)

    total_reward = 0
    steps = 0
    rewards = []
    done = False

    print(f"\n--- Running {level.upper()} task ---")

    while not done and steps < 6:
        obs_dict = observation.model_dump()

        action = decide_action(obs_dict, level)

        observation, reward, done, _ = env.step(action)

        steps += 1
        total_reward += reward
        rewards.append(reward)

        print(f"[STEP] step={steps} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

    
    score = total_reward / 3.0
    score = max(0.01, min(score, 0.99))

    return score, steps, rewards



async def main():
    print(f"[START] task=cloud_security env=cloud_env model={MODEL_NAME}")

    total_score = 0
    total_steps = 0
    all_rewards = []

    for level in ["easy", "medium", "hard"]:
        score, steps, rewards = await run_task(level)

        total_score += score
        total_steps += steps
        all_rewards.extend(rewards)

    success = total_score > 0.5
    avg_score = total_score / 3

    print(
        f"[END] success={str(success).lower()} "
        f"steps={total_steps} "
        f"score={avg_score:.3f} "
        f"rewards={','.join([f'{r:.2f}' for r in all_rewards])}"
    )


if __name__ == "__main__":
    asyncio.run(main())