from flask import Flask, jsonify
from simulation.tasks import get_task
from simulation.models import Action
import threading

app = Flask(__name__)

def choose_action(obs):
    target = 30
    error = target - obs.concentration
    dose = max(0, min(20, error * 0.4))
    return round(dose, 2)

def run_episode(task_name):
    env = get_task(task_name)
    obs = env.reset()
    results = []
    done = False
    while not done:
        dose = choose_action(obs)
        action = Action(dose=dose)
        obs, reward, done, _ = env.step(action)
        results.append({"dose": dose, "reward": round(reward, 2), "done": done})
    return results

@app.route("/")
def index():
    return jsonify({"status": "running", "message": "Medication Dosing Env is live!"})

@app.route("/run/<task_name>")
def run(task_name):
    results = run_episode(task_name)
    return jsonify({"task": task_name, "steps": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)