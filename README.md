---
title: Cloud Security Fixer
emoji: "🌍"
colorFrom: blue
colorTo: green
sdk: docker
---

# ☁️ Cloud Security Misconfiguration Environment (OpenEnv)

## ⚡ What this environment tests

This environment evaluates how well an AI agent can handle real-world cloud security incidents involving multiple misconfigurations, hidden vulnerabilities, and sequential decision-making.

Unlike simple benchmarks, agents must not only fix issues but also adapt when new risks emerge after partial fixes.

  This environment is designed as a lightweight benchmark for evaluating real-world decision-making in cloud security systems.

---

## 🚀 Overview

This project is my attempt to build something practical instead of a typical toy environment.

I created a cloud security simulation where an AI agent interacts with real-world issues like exposed storage, open ports, and risky IAM permissions. The goal is simple — the agent should understand the situation, fix all the issues step-by-step, and only then verify that everything is secure.

What makes it interesting is that problems don’t appear one at a time anymore — **multiple misconfigurations can exist together**, just like in real cloud setups.

---

## 💡 Why I built this

While learning cloud security, I noticed that most examples are theoretical. But in real systems, small mistakes like:

- Public S3 buckets  
- Open SSH ports  
- Over-permissive IAM policies  

can combine and create serious vulnerabilities.

So instead of just studying them, I wanted to simulate them in a way where an AI agent actually has to **think, decide, and act in sequence** — similar to how a real engineer would.

---

## ⚙️ How the environment works

The environment follows the OpenEnv structure:

- `reset()` → starts a new scenario  
- `step(action)` → agent performs an action  
- `state()` → returns current state  

Each step gives feedback based on how useful the action is.

---

## 🧪 Task Design

There are 3 levels of difficulty:

---

### 🟢 Easy
- Single issue (e.g., public S3 bucket)
- Agent needs to fix and verify

---

### 🟡 Medium
- Two issues at the same time:
  - Public S3 bucket  
  - Open port 22  
- Agent must fix both before verifying

---

### 🔴 Hard
- Three issues together:
  - Public S3 bucket  
  - Open port 22  
  - Over-permissive IAM policy  

This requires **multi-step reasoning and correct sequencing**.

---

## 🔄 Example Scenario (Hard)

**Resources:**
- S3 bucket is public  
- EC2 port 22 is open  
- IAM policy allows admin access  

**Expected behavior:**
1. Fix S3 bucket  
2. Close port 22  
3. Restrict IAM policy  
4. Verify fix

## 🔥 What makes this different

Instead of a simple one-step reward system, this environment introduces:

- Multiple issues at once  
- Sequential fixing requirement  
- Verification only after all issues are solved  
- Partial rewards for progress  

In some scenarios, not all issues are visible initially. New vulnerabilities may appear after partial fixes, requiring the agent to adapt dynamically.
This makes it closer to real-world workflows rather than just pattern matching.

---

## 🧩 Hidden System Behavior (Advanced Design)

To simulate real-world cloud complexity, the environment includes **hidden cascading issues**.

For example:
- Fixing a public S3 bucket may expose an IAM misconfiguration
- Some vulnerabilities only appear after initial fixes

This forces the agent to:
- Adapt dynamically
- Perform multi-step reasoning
- Handle non-obvious dependencies

This mirrors how real cloud systems behave under security changes.


---

## 🧠 Reward System

| Action Type       | Reward |
|-------------------|--------|
| Correct fix       | +0.6 to +0.8 |
| Hidden issue fix  | +0.6 |
| Final verification| +0.9 |
| Wrong action      | -0.1 |

This gives continuous feedback across the full episode instead of only success/failure.

---

## 🎯 Reward Design Philosophy

Instead of binary rewards, this environment uses **progressive reward shaping**:

- Encourages correct fixes
- Penalizes repeated or irrelevant actions
- Rewards verification separately

This ensures:
- Better learning signal across steps
- Reduced exploitation of simple strategies
- More realistic agent evaluation

---
## 🤖 Baseline Agent

The `inference.py` script runs a simple agent that:

- Handles all 3 tasks (easy → medium → hard)
- Fixes issues step-by-step
- Verifies only after all fixes
- Produces structured logs: [START] [STEP] [END]

---

## 🧠 Design Thinking

This environment was designed with a focus on:

- Real-world cloud security workflows
- Sequential problem solving
- Hidden dependencies between resources
- Deterministic and reproducible evaluation

Rather than building a complex system, the goal was to create a **clean, reliable benchmark** that still captures real-world behavior.

---

## 🐳 Deployment

The environment is deployed using Docker on Hugging Face Spaces.

Endpoints:

- `POST /reset`
- `POST /step`

Swagger UI:/docs
---

## 📁 Project Structure
  cloud_env/ data/ server.py inference.py Dockerfile openenv.yaml requirements.txt README.md

---

## 🧩 Future Improvements

- Dynamic cloud scenarios  
- Interdependent vulnerabilities  
- Real log-based simulations  
- Multi-agent collaboration  
- Policy-driven security enforcement  

---

## 🏁 Final Thoughts

This project helped me understand how AI agents can be evaluated on real-world problems instead of just simple or game-based environments.

I tried to keep it practical, understandable, and close to real cloud scenarios without overcomplicating it.

---

⭐ Thanks for checking it out!