# Smart Basketball Shooter — BAI701 Batch B1

An interactive basketball shooting game and analytics dashboard demonstrating the **epsilon-greedy multi-armed bandit** algorithm.

## Features
- Five shooting zones represented as bandit arms.
- Manual shots and autonomous agent shots.
- Epsilon-greedy, decaying epsilon-greedy, greedy, random and UCB policies.
- Incremental sample-average action-value estimates.
- Exploration/exploitation telemetry, points, accuracy, streaks and recent decision log.
- Reward history chart and reproducible strategy benchmark.
- Python Flask REST API with HTML, CSS and vanilla JavaScript frontend.

## Requirements
- Python 3.9+
- Flask (installed from `requirements.txt`)

## Run on Windows / VS Code
Open this folder in VS Code, then in the terminal:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## How to demonstrate
1. Click each of the five court positions to make manual shots.
2. Choose **ε-Greedy** and click **Let AI shoot** repeatedly.
3. Watch the estimated reward, exploration/exploitation bars and reward chart update.
4. Try **Decaying ε-Greedy**, **Greedy**, **Random** and **UCB**.
5. Click **Run benchmark** to compare all five strategies over 1,500 simulated shots each.
6. Reset to start a fresh interactive session.

## Reinforcement learning model
Each shooting zone is an arm. The environment samples a make/miss outcome using a hidden probability. The agent does not receive the probabilities; it only observes the reward (3 for a made shot, 0 for a miss).

Sample-average action-value update:

`Q(a) <- Q(a) + (R - Q(a)) / N(a)`

For epsilon-greedy, the agent selects a random arm with probability epsilon and otherwise selects an arm with the largest estimated value. Decaying epsilon begins at 0.20 and reduces gradually to a 0.02 floor. The benchmark uses a fixed seed for repeatability; results are simulated, not real basketball statistics.

## API
- `GET /api/state` — current public game state
- `POST /api/shot` — manual shot: `{"position":"top_key"}`
- `POST /api/agent-shot` — agent decision: `{"strategy":"epsilon_greedy"}`
- `POST /api/train` — train for 1–10,000 rounds: `{"rounds":500,"strategy":"decaying_epsilon"}`
- `POST /api/reset` — reset session
- `GET /api/benchmark` — compare five strategies

## Tests
```bash
python -m unittest discover -s tests -v
```

## Important academic note
This is a **multi-armed bandit** example: every shot is a repeated choice among actions with unknown reward distributions, with no changing state required for the assigned core algorithm. It is not a full state-based basketball simulator or deep Q-network.

## Team
Batch B1 — add/verify all five student names and USNs from the official activity sheet before submission.
