from fastapi import FastAPI
from env.environment import CloudEnv

app = FastAPI()
env = CloudEnv()

@app.post("/reset")
def reset():
    state = env.reset()
    return {
        "observation": state,
        "reward": 0.0,
        "done": False,
        "info": {}
    }

from env.models import Action

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action.action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }