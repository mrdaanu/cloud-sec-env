from fastapi import FastAPI
from env.environment import CloudEnv
from env.models import Action
import uvicorn

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
    obs, reward, done, info = env.step(action.action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=7860)