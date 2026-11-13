from flask import Flask, jsonify, render_template, request
from bandit import BasketballBandit

app = Flask(__name__)
game = BasketballBandit()

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/api/state')
def state():
    return jsonify(game.public_state())

@app.post('/api/shot')
def shot():
    data = request.get_json(silent=True) or {}
    try:
        arm = data.get('position')
        result = game.shoot(arm, strategy=data.get('strategy', 'epsilon_greedy'))
        return jsonify(result)
    except (ValueError, KeyError) as exc:
        return jsonify({'error': str(exc)}), 400

@app.post('/api/agent-shot')
def agent_shot():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify(game.agent_shot(data.get('strategy', 'epsilon_greedy')))
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

@app.post('/api/train')
def train():
    data = request.get_json(silent=True) or {}
    try:
        rounds = int(data.get('rounds', 100))
        strategy = data.get('strategy', 'epsilon_greedy')
        return jsonify(game.train(rounds, strategy))
    except (ValueError, TypeError) as exc:
        return jsonify({'error': str(exc)}), 400

@app.post('/api/reset')
def reset():
    game.reset()
    return jsonify(game.public_state())

@app.get('/api/benchmark')
def benchmark():
    return jsonify(BasketballBandit.benchmark())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
