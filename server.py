from fastapi import FastAPI
from cloud_env.environment import CloudEnv
from cloud_env.models import Action

app = FastAPI()
env = CloudEnv()


@app.get("/")
def home():
    return {"message": "Cloud Security Environment Running"}


@app.post("/reset")
def reset():
    obs = env.reset()

    return {
        "observation": obs.model_dump(),   # ✅ FIXED
        "reward": 0.0,
        "done": False,
        "info": {}
    }


@app.post("/step")
def step(action: Action):
    try:
        obs, reward, done, info = env.step(action.action)

        return {
            "observation": obs.model_dump(),   # ✅ FIXED
            "reward": float(reward),           # ✅ ensure float
            "done": bool(done),                # ✅ ensure bool
            "info": info if isinstance(info, dict) else {}
        }

    except Exception as e:
        # ✅ IMPORTANT: STILL RETURN VALID FORMAT
        return {
            "observation": {
                "resources": [],
                "issues_found": [],
                "step_count": 0
            },
            "reward": -0.1,
            "done": True,
            "info": {"error": str(e)}
        }