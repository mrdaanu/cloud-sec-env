---
title: Cloud Security Fixer
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
app_file: server.py
pinned: false
---

# Cloud Security Misconfiguration Fixer

This project simulates a real-world cloud security environment where an AI agent detects and fixes misconfigurations.

## Features

- Detects public S3 buckets
- Identifies open ports in EC2
- Fixes insecure IAM policies
- Deterministic reward system
- Multi-level tasks (easy, medium, hard)

## Tasks

- Easy: Fix public S3 bucket
- Medium: Close open port
- Hard: Restrict IAM policy

## Usage

API endpoints:
- `/reset`
- `/step`

## Why it matters

Cloud misconfigurations are a major security risk. This environment helps evaluate AI agents in real DevSecOps workflows.