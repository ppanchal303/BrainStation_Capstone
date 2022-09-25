from pickletools import float8
import gym
from gym import spaces
import numpy as np

# import gameAI

# from gym_game.envs import gameAI
from gym_game.envs.gameAI import *
# from gameAI import *
from gym_game.envs.gameAI_hard import *
# from gameAI_hard import *

# import gameAgent



class CustomEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode = None):
        self.game = SnakeGameAI(WIDTH, HEIGHT)
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=np.array([0,0,0]), high=np.array([8,4,8]), dtype=np.int32)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window = None
        self.clock = None

    def reset(self):
        del self.game
        self.game = SnakeGameAI(WIDTH, HEIGHT)
        state = self.game.get_state(self.game)

        if self.render_mode == "human":
            self.game.draw_game()

        return state

    def step(self, action):
        reward, done, score = self.game.game_step(action)
        state = self.game.get_state(self.game)

        if self.render_mode == "human":
            self.game.draw_game()

        return state, reward, done, False, {"Score": score}

    def render(self, mode="human", close=False):
        self.game.draw_game()

    def close(self):
        # if self.window is not None:
            pygame.display.quit()
            pygame.quit()

class CustomEnv_hard(gym.Env):
    metadata = {'render_modes' : ['human']}
    def __init__(self, render_mode = None):
        self.game = SnakeGameAI_hard(WIDTH, HEIGHT)
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=np.array([0,0,0]), high=np.array([8,4,8]), dtype=np.int32)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window = None
        self.clock = None

    def reset(self):
        del self.game
        self.game = SnakeGameAI_hard(WIDTH, HEIGHT)
        state = self.game.get_state(self.game)
        
        if self.render_mode == "human":
            self.game.draw_game()

        return state

    def step(self, action):
        reward, done, score = self.game.game_step(action)
        state = self.game.get_state(self.game)
        
        if self.render_mode == "human":
            self.game.draw_game()

        return state, reward, done, False, {"Score": score}

    def render(self, mode="human", close=False):
        self.game.draw_game()

    def close(self):
        # if self.window is not None:
            pygame.display.quit()
            pygame.quit()

# def main():
#     a = spaces.Box(low=np.array([0,0,0]), high=np.array([7,3,7]), dtype=np.int32)
#     # print(a.low)
#     b = spaces.Discrete(3)
#     print(b.sample())

#     state_low = a.low
#     state_high = a.high
#     # state_shape = env.observation_space.shape
#     # print(f"State range: {state_low}, {state_high}")
#     state_size = state_high - state_low

#     qtable = np.zeros(*state_size,b.n)

#     print(qtable)

#     g = SnakeGameAI()

#     st = g.get_state()




# if __name__ == "__main__":
#     main()