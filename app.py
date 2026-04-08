from flask import Flask, jsonify, request
from simulation.tasks import get_task
from simulation.models import Action
import os

app = Flask(__name__)

# Store active environments
envs = {}

@app.route("/")
def index():
    return jsonify({"status": "running", "message": "Medication Dosing Env is live!"})

@app.route("/reset", methods=["POST"])
def reset():
    data = request.get_json() or {}
    task_name = data.get("task", "easy")
    env = get_task(task_name)
    obs = env.reset()
    envs["current"] = env
    return jsonify({"observation": {"concentration": obs.concentration}})

@app.route("/step", methods=["POST"])
def step():
    data = request.get_json() or {}
    dose = float(data.get("dose", 0.0))
    env = envs.get("current")
    if env is None:
        return jsonify({"error": "Environment not initialized. Call /reset first."}), 400
    action = Action(dose=dose)
    obs, reward, done, info = env.step(action)
    return jsonify({
        "observation": {"concentration": obs.concentration},
        "reward": reward,
        "done": done,
        "info": info
    })

@app.route("/close", methods=["POST"])
def close():
    env = envs.get("current")
    if env:
        env.close()
        envs.pop("current", None)
    return jsonify({"status": "closed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)