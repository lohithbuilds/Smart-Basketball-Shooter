# SMART BASKETBALL SHOOTER
## An ε-Greedy Multi-Armed Bandit Reinforcement Learning Application

**Course:** BAI701 — Deep Learning and Reinforcement Learning  
**Academic Year:** 2026–27  
**Batch:** B1  
**Institution:** K. S. Institute of Technology, Department of AIML

> Complete the team member names, USNs, guide details, screenshots and measured benchmark results before submission.

## 1. Abstract
Smart Basketball Shooter is an interactive reinforcement learning demonstration in which an agent learns which of five basketball shooting positions gives the highest expected reward. Each position is treated as an arm of a multi-armed bandit. The agent initially explores different positions and increasingly exploits positions with higher estimated rewards. The application includes a browser-based basketball game, a Python backend and an analytics dashboard that visualizes reward, accuracy, action-value estimates and exploration-versus-exploitation behaviour.

## 2. Problem Statement
Develop an intelligent agent that selects a shooting position from multiple alternatives when the reward distribution of each position is initially unknown. The agent must balance exploration and exploitation to maximize cumulative reward over repeated shots.

## 3. Objectives
1. Model five basketball shooting positions as bandit actions.
2. Keep the true shot-success probabilities hidden from the agent.
3. Implement ε-greedy action selection and sample-average reward estimates.
4. Implement decaying ε and comparison strategies (random, greedy and UCB).
5. Record cumulative points, shot accuracy and decision counts.
6. Visualize learning behaviour in an interactive analytics dashboard.

## 4. Environment Design
The environment contains five shooting positions: Left Corner, Left Wing, Top of Key, Right Wing and Right Corner. The simulator uses hidden success probabilities to generate made or missed shots. These probabilities are part of the environment only and are not exposed in the agent's observation. A made three-point shot gives +3 reward; a missed shot gives 0 reward.

## 5. Reinforcement Learning Formulation
- **Agent:** Basketball shooting decision-maker.
- **Environment:** Simulated basketball court and shot outcome generator.
- **Actions:** Select one of five shooting positions.
- **Reward:** +3 for a made shot, 0 for a miss.
- **Action-value estimate:** Estimated average reward for each position.
- **Policy:** ε-greedy; explore randomly with probability ε, otherwise exploit the highest estimated action value.

## 6. Algorithm
For selected action a, update the estimate using:

`Q(a) ← Q(a) + [R − Q(a)] / N(a)`

where Q(a) is the estimated reward, R is the observed reward and N(a) is the number of times action a has been selected. In the decaying strategy, ε starts at 0.20 and gradually decreases, with a lower bound of 0.02.

## 7. System Architecture
Browser (HTML/CSS/JavaScript game and dashboard) ↔ Flask REST API (Python) ↔ Bandit environment and agent (action selection, reward sampling, value updates, benchmark).

## 8. Implementation
The frontend provides manual shot selection, autonomous agent shots, strategy selection, a reset option, live metrics, reward history and a strategy benchmark. The backend exposes JSON endpoints for state, shots, training, reset and benchmarking.

## 9. Results and Analysis
Insert screenshots and actual output from the benchmark. Compare total points, accuracy and the estimated best shooting position for Random, Greedy, ε-Greedy, Decaying ε-Greedy and UCB. Repeat experiments with multiple random seeds for a stronger evaluation. Do not present a single simulation as a universal result.

## 10. Conclusion
The project demonstrates how an ε-greedy multi-armed bandit agent learns from reward feedback without being told which shooting position is best. The dashboard makes exploration, exploitation and estimated action values observable. The simulator is intentionally a bandit model rather than a full basketball physics simulation.

## 11. Future Enhancements
- Add shot distance, defender pressure and fatigue as context features.
- Model time-varying shot probabilities.
- Add a contextual bandit or state-based reinforcement learning extension.
- Export experiment results as CSV and support multiple-seed reports.
