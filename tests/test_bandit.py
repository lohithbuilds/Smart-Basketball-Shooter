import unittest
from bandit import BasketballBandit

class BanditTests(unittest.TestCase):
    def test_reset_state(self):
        env = BasketballBandit()
        self.assertEqual(env.total_shots, 0)
        self.assertEqual(len(env.public_state()['positions']), 5)

    def test_shot_updates_statistics(self):
        env = BasketballBandit(seed=7)
        result = env.shoot('top_key')
        state = result['state']
        self.assertEqual(state['total_shots'], 1)
        self.assertEqual(state['makes'] + state['misses'], 1)
        self.assertEqual(state['positions'][2]['shots'], 1)

    def test_training_round_count(self):
        env = BasketballBandit(seed=11)
        result = env.train(50, 'epsilon_greedy')
        self.assertEqual(result['total_shots'], 50)

    def test_invalid_arm(self):
        env = BasketballBandit()
        with self.assertRaises(ValueError):
            env.shoot('half_court')

    def test_hidden_probabilities(self):
        env = BasketballBandit()
        self.assertNotIn('probability', str(env.public_state()))

if __name__ == '__main__':
    unittest.main()
