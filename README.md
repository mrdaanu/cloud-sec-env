---
title: Cloud Security Fixer
emoji: "🌍"
colorFrom: blue
colorTo: green
sdk: docker
---

# ☁️ Cloud Security Misconfiguration Environment (OpenEnv)

## ⚡ Why this environment exists

Most AI evaluation environments test whether an agent can solve a problem.

But in real-world cloud security, that's not enough.

Engineers don’t just fix issues once — they often:
- Miss hidden vulnerabilities  
- Apply incomplete fixes  
- Verify too early  
- Get feedback, and then adapt  

This environment was designed to simulate that exact workflow.

Instead of a static "fix → success" system, this environment introduces:

- Multiple simultaneous misconfigurations  
- Hidden vulnerabilities that appear during runtime  
- Penalization for premature verification  
- Adaptive reward feedback across steps  

The goal is not just to test correctness —  
but to evaluate **decision-making under uncertainty**.

---

## 🚀 Overview

This project simulates real-world cloud security scenarios where an AI agent must:

- Identify vulnerabilities  
- Fix them in the correct sequence  
- Handle unexpected issues  
- Verify only when the system is fully secure  

The environment is inspired by common cloud mistakes like:

- Public S3 buckets  
- Open SSH ports  
- Over-permissive IAM policies  

---

## 🧠 What makes this environment different

This is not a simple or deterministic benchmark.

An agent interacting with this environment must:

- Solve multiple issues step-by-step  
- Avoid verifying too early  
- Recover from failed attempts  
- Adapt when new vulnerabilities appear  

### Example behavior

Fix S3 → Close port → Verify ❌  
Fix IAM → Verify ✅  

This reflects how real engineers debug and secure systems.

---

## 🧪 Task Design

### 🟢 Easy
- Single issue (S3 public)
- Fix → Verify

---

### 🟡 Medium
- Multiple issues:
  - S3 public  
  - EC2 port open  
- Possible hidden IAM issue  
- Agent must adapt if verification fails  

---

### 🔴 Hard
- All issues present:
  - S3 public  
  - EC2 open port  
  - IAM over-permission  
- Requires full multi-step reasoning  

---

## 🔄 Hidden State (Advanced Behavior)

Some scenarios introduce **hidden vulnerabilities**:

- IAM issues may not be visible initially  
- They appear only after partial fixes  

This forces the agent to:
- Re-evaluate decisions  
- Adapt after failure  
- Avoid overconfidence  

---

## 🧠 Reward System

| Action Type        | Reward |
|------------------|--------|
| Fix S3            | 0.56   |
| Fix EC2           | 0.57   |
| Fix IAM           | 0.59   |
| Verify (correct)  | 0.88   |
| Wrong / Early     | 0.06   |

### Design Philosophy

- Rewards are always between **0 and 1**  
- No binary success/failure  
- Encourages progress and learning  
- Penalizes premature decisions  

---

## 🤖 Baseline Agent

The `inference.py` script runs an agent that:

- Solves all 3 tasks (easy → medium → hard)  
- Follows correct fix sequence  
- Detects failed verification  
- Adapts to hidden issues  

Logs follow strict format:

[START]  
[STEP]  
[END]  

---

## ⚙️ Environment API

The environment follows OpenEnv specification:

- `reset()` → initializes scenario  
- `step(action)` → applies action  
- `state()` → returns current state  

---

## 🐳 Deployment

This environment is deployed using Docker on Hugging Face Spaces.

Endpoints:

- `POST /reset`  
- `POST /step`  

Swagger UI available at:
`/docs`

---

## 📁 Project Structure

cloud_env/  
data/  
server.py  
inference.py  
Dockerfile  
openenv.yaml  
requirements.txt  
README.md  

---

## 🎯 Why this matters

Most environments test if an agent can solve a task.

This one tests:

- Multi-step reasoning  
- Sequential decision-making  
- Failure recovery  
- Adaptive intelligence  

It can be used as a benchmark for:

- Autonomous security agents  
- DevOps automation systems  
- AI decision-making evaluation  

---

## 🧠 Design Thinking

This environment was built with focus on:

- Real-world cloud workflows  
- Deterministic yet adaptive behavior  
- Clear reward signals  
- Minimal but meaningful complexity  

The goal was not to overcomplicate —  
but to create something **practical, testable, and realistic**.

---

## 🏁 Final Thoughts

This project started as a simple idea:

"What if an AI agent could fix cloud security issues?"

But it evolved into something deeper:

- An agent that can fail  
- Learn from that failure  
- And then correct itself  

That’s closer to real intelligence than just solving a fixed task.

---

⭐ Thanks for checking it out!