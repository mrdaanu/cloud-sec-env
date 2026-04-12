from fastapi import FastAPI
from pydantic import BaseModel
from cloud_env.environment import CloudEnv

# 🚀 CLEAN PROFESSIONAL FASTAPI APP
app = FastAPI(
    title="Cloud Security Fixer Environment",
    description="""
    🚀 A realistic Reinforcement Learning environment for cloud security remediation.

    This environment simulates real-world cloud misconfigurations such as:
    - Public S3 buckets
    - Open SSH ports (EC2)
    - Over-permissive IAM policies

    🧠 Agent Responsibilities:
    - Identify security issues
    - Apply correct fixes step-by-step
    - Verify final system state

    🎯 Designed for evaluating autonomous AI agents in DevOps & cybersecurity workflows.
    """,
    version="1.0.0"
)

# 🔄 GLOBAL ENV INSTANCE
env = CloudEnv()


# 📦 REQUEST MODEL
class ActionRequest(BaseModel):
    action: str


# 🏠 HOME ROUTE
@app.get("/", tags=["Info"])
def home():
    return {
        "message": "Cloud Security Fixer Environment is running 🚀",
        "endpoints": {
            "reset": "POST /reset",
            "step": "POST /step"
        }
    }


# 🔄 RESET ENVIRONMENT
@app.post("/reset", tags=["Environment"])
def reset(level: str = "easy"):
    observation = env.reset(level)
    return observation


# ⚡ STEP ACTION
@app.post("/step", tags=["Environment"])
def step(req: ActionRequest):
    observation, reward, done, info = env.step(req.action)
    return {
        "observation": observation,
        "reward": reward,
        "done": done,
        "info": info
    }