import asyncio
from env.environment import CloudEnv


def decide_action(observation, already_fixed):
    resources = observation["resources"]

    for r in resources:

        if r["type"] == "s3" and "fix_s3" not in already_fixed:
            return "Make S3 bucket private"

        elif r["type"] == "ec2" and "fix_ec2" not in already_fixed:
            return "Close port 22"

        elif r["type"] == "iam" and "fix_iam" not in already_fixed:
            return "Apply least privilege IAM policy"

    return "No action"


async def run_task(level):
    env = CloudEnv()
    observation = env.reset(level)

    total_reward = 0
    steps = 0
    rewards = []
    done = False

    fixed = []

    while not done and steps < 6:
        obs_dict = observation.model_dump()

        action = decide_action(obs_dict, fixed)

        observation, reward, done, _ = env.step(action)

        if reward == 1.0:
            parsed = action.lower()
            if "s3" in parsed:
                fixed.append("fix_s3")
            elif "port" in parsed:
                fixed.append("fix_ec2")
            elif "iam" in parsed:
                fixed.append("fix_iam")

        steps += 1
        total_reward += reward
        rewards.append(f"{reward:.2f}")

        print(f"[STEP] step={steps} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

    return total_reward, steps, rewards


async def main():
    print("[START] task=cloud_security env=cloud_env model=multi-step-agent")

    total_score = 0
    total_steps = 0
    all_rewards = []

    for level in ["easy", "medium", "hard"]:
        score, steps, rewards = await run_task(level)

        total_score += score
        total_steps += steps
        all_rewards.extend(rewards)

    success = total_score >= 3.0
    avg_score = total_score / 3

    print(f"[END] success={str(success).lower()} steps={total_steps} score={avg_score:.3f} rewards={','.join(all_rewards)}")


if __name__ == "__main__":
    asyncio.run(main())