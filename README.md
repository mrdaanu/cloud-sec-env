---

title: Cloud Security Fixer
emoji: 🌍
colorFrom: blue
colorTo: green
sdk: docker

☁️ Cloud Security Misconfiguration Environment

🚀 Overview

This project is my attempt to build something practical instead of a typical toy environment.

I created a cloud security simulation where an AI agent interacts with common real-world issues like exposed storage, open ports, and risky IAM permissions. The goal is simple — the agent should understand the problem, fix it, and then verify that the fix actually worked.

---

💡 Why I built this

While learning about cloud security, I realized that most examples are theoretical. But in reality, small mistakes like:

- Public S3 buckets
- Open SSH ports
- Over-permissive IAM policies

can lead to serious problems.

So instead of just studying them, I thought — why not simulate them and let an AI agent handle them step by step?

---

⚙️ How the environment works

The environment follows a simple structure:

- "reset()" → starts a new scenario
- "step(action)" → agent performs an action
- "state()" → returns current state

Each step gives feedback based on how good the action is.

---

🧪 Tasks

I designed three levels of difficulty:

🟢 Easy

- Problem: Public S3 bucket
- Goal: Make it private

🟡 Medium

- Problem: Port 22 is open
- Goal: Close the port

🔴 Hard

- Problem: IAM policy is too permissive
- Goal: Apply least privilege

---

🔥 What makes this different

Instead of giving reward in one step, I added a two-step system:

1. First fix the issue
2. Then verify the fix

Example:

- Fix → reward = 0.7
- Verify → reward = 1.0

This makes it feel closer to how real engineers work.

---

🧠 Reward System

Action Type| Reward
Correct fix| 0.7
Verify step| 1.0
Partial action| 0.3
Wrong action| -0.1

The idea was to give continuous feedback instead of just success/failure.

---

🤖 Baseline Agent

I also built a simple agent in "inference.py" that:

- Runs all tasks (easy → hard)
- Follows fix → verify flow
- Produces consistent output

Logs look like:

[START]
[STEP]
[END]

---

🐳 Deployment

The project is deployed on Hugging Face Spaces using Docker.

You can test it using:

- "POST /reset"
- "POST /step"

Swagger UI is available at "/docs".

---

📁 Project Structure

env/
data/
server.py
inference.py
Dockerfile
openenv.yaml
requirements.txt
README.md

---

🏁 Final Thoughts

This project helped me understand how AI agents can be tested on real-world problems, not just games or simple tasks.

I tried to keep it simple, practical, and meaningful rather than overcomplicated.

---

⭐ Thanks for checking it out!