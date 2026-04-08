---
title: Cloud Security Fixer
emoji: 🌍
colorFrom: blue
colorTo: green
sdk: docker
---

# ☁️ Cloud Security Misconfiguration Environment (OpenEnv)

## 🚀 Overview

This environment simulates real-world cloud security misconfigurations that DevOps and security engineers handle daily.

It enables AI agents to:
- Detect vulnerabilities
- Take corrective actions
- Receive graded feedback

---

## 🧠 Why this matters

Cloud misconfigurations cause:
- Data leaks (public S3)
- Unauthorized access (open ports)
- Privilege escalation (IAM policies)

This environment provides a **realistic evaluation benchmark** for AI agents.

---

## ⚙️ Environment Design

### Observation Space

```json
{
  "resources": [...],
  "issues_found": [...],
  "step_count": int
}