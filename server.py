from fastapi import FastAPI
from env.environment import CloudEnv
from env.models import Action

app = FastAPI()
env = CloudEnv()


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs,
        "reward": 0.0,
        "done": False,
        "info": {}
    }


@app.post("/step")
def step(action: Action):
    try:
        obs, reward, done, info = env.step(action.action)

        return {
            "observation": obs,
            "reward": reward,
            "done": done,
            "info": info
        }

    except Exception as e:
        return {
            "error": str(e)
        }