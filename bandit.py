"""Multi-armed bandit environment for a basketball shooting game."""
from __future__ import annotations
import random
from copy import deepcopy

class BasketballBandit:
    # Environment-only probabilities: the agent never receives these values.
    POSITIONS = [
        {'id': 'left_corner', 'name': 'Left Corner', 'short': 'LC', 'points': 3, 'probability': 0.42},
        {'id': 'left_wing', 'name': 'Left Wing', 'short': 'LW', 'points': 3, 'probability': 0.55},
        {'id': 'top_key', 'name': 'Top of Key', 'short': 'TOP', 'points': 3, 'probability': 0.68},
        {'id': 'right_wing', 'name': 'Right Wing', 'short': 'RW', 'points': 3, 'probability': 0.51},
        {'id': 'right_corner', 'name': 'Right Corner', 'short': 'RC', 'points': 3, 'probability': 0.38},
    ]
    STRATEGIES = {'epsilon_greedy', 'decaying_epsilon', 'greedy', 'random', 'ucb'}

    def __init__(self, seed=42):
        self.seed = seed
        self.reset()

    def reset(self):
        self.rng = random.Random(self.seed)
        self.counts = {p['id']: 0 for p in self.POSITIONS}
        self.values = {p['id']: 0.0 for p in self.POSITIONS}
        self.total_shots = 0
        self.total_points = 0
        self.makes = 0
        self.misses = 0
        self.explorations = 0
        self.exploitations = 0
        self.epsilon = 0.20
        self.history = []
        self.rewards = []
        self.best_streak = 0
        self.current_streak = 0
        return self.public_state()

    def _position(self, arm):
        for p in self.POSITIONS:
            if p['id'] == arm:
                return p
        raise ValueError('Choose a valid shooting position.')

    def choose_action(self, strategy='epsilon_greedy'):
        if strategy not in self.STRATEGIES:
            raise ValueError('Unknown strategy.')
        ids = [p['id'] for p in self.POSITIONS]
        if strategy == 'random':
            return self.rng.choice(ids), 'exploration'
        if strategy == 'ucb':
            untried = [a for a in ids if self.counts[a] == 0]
            if untried:
                return self.rng.choice(untried), 'exploration'
            import math
            scores = {a: self.values[a] + (2 * math.log(max(1, self.total_shots)) / self.counts[a]) ** 0.5 for a in ids}
            best = max(scores.values())
            return self.rng.choice([a for a in ids if scores[a] == best]), 'exploitation'
        if strategy == 'decaying_epsilon':
            self.epsilon = max(0.02, 0.20 * (0.995 ** self.total_shots))
        elif strategy == 'greedy':
            self.epsilon = 0.0
        elif strategy == 'epsilon_greedy':
            self.epsilon = 0.20
        if self.rng.random() < self.epsilon:
            return self.rng.choice(ids), 'exploration'
        best = max(self.values.values())
        # Random tie-breaking avoids always favoring the first arm at initialization.
        return self.rng.choice([a for a in ids if self.values[a] == best]), 'exploitation'

    def shoot(self, arm, strategy='manual'):
        p = self._position(arm)
        made = self.rng.random() < p['probability']
        reward = p['points'] if made else 0
        self.total_shots += 1
        self.total_points += reward
        self.makes += int(made)
        self.misses += int(not made)
        self.counts[arm] += 1
        n = self.counts[arm]
        self.values[arm] += (reward - self.values[arm]) / n
        if made:
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
        else:
            self.current_streak = 0
        if strategy == 'exploration':
            self.explorations += 1
        elif strategy == 'exploitation':
            self.exploitations += 1
        entry = {'shot': self.total_shots, 'position': p['name'], 'position_id': arm,
                 'made': made, 'reward': reward, 'decision': strategy,
                 'estimated_value': round(self.values[arm], 3)}
        self.history.append(entry)
        self.rewards.append(reward)
        return {'result': entry, 'state': self.public_state()}

    def agent_shot(self, strategy='epsilon_greedy'):
        arm, decision = self.choose_action(strategy)
        return self.shoot(arm, decision)

    def train(self, rounds=100, strategy='epsilon_greedy'):
        if not 1 <= rounds <= 10000:
            raise ValueError('Rounds must be between 1 and 10,000.')
        if strategy not in self.STRATEGIES:
            raise ValueError('Unknown strategy.')
        start = self.total_shots
        for _ in range(rounds):
            self.agent_shot(strategy)
        state = self.public_state()
        state['training_rounds'] = rounds
        state['range_start'] = start + 1
        return state

    def public_state(self):
        # Deliberately omit true probabilities to preserve the unknown-reward setup.
        positions = [{'id': p['id'], 'name': p['name'], 'short': p['short'], 'points': p['points'],
                      'shots': self.counts[p['id']], 'estimated_reward': round(self.values[p['id']], 3)}
                     for p in self.POSITIONS]
        return {'positions': positions, 'total_shots': self.total_shots,
                'total_points': self.total_points, 'makes': self.makes, 'misses': self.misses,
                'accuracy': round(100 * self.makes / self.total_shots, 1) if self.total_shots else 0,
                'average_reward': round(self.total_points / self.total_shots, 3) if self.total_shots else 0,
                'explorations': self.explorations, 'exploitations': self.exploitations,
                'exploration_pct': round(100*self.explorations/max(1,self.explorations+self.exploitations),1),
                'exploitation_pct': round(100*self.exploitations/max(1,self.explorations+self.exploitations),1),
                'epsilon': round(self.epsilon, 4), 'best_streak': self.best_streak,
                'history': deepcopy(self.history[-20:]), 'reward_history': self.rewards[-200:]}

    @classmethod
    def benchmark(cls, rounds=1500, seed=2026):
        results = []
        for strategy in ['random', 'greedy', 'epsilon_greedy', 'decaying_epsilon', 'ucb']:
            env = cls(seed=seed)
            env.train(rounds, strategy)
            results.append({'strategy': strategy, 'label': strategy.replace('_', ' ').title(),
                            'points': env.total_points, 'accuracy': env.public_state()['accuracy'],
                            'shots': env.total_shots, 'best_position': max(env.values, key=env.values.get),
                            'estimated_rewards': {k: round(v, 3) for k,v in env.values.items()}})
        return {'rounds': rounds, 'results': results}
