######################################################
# Project: Snake Game                                #
# Author: Pranav Panchal                             #
# Date: 12/09/2022                                   # 
######################################################                               
# This generates the environment for the snake games #
# in accordance with gym library                     #
######################################################


# Importing dependencies
from pickletools import float8
import gym
from gym import spaces
import numpy as np
from gym_game.envs.gameAI import *
from gym_game.envs.gameAI_hard import *

class CustomEnv(gym.Env):
    '''
    This helps to initialise the custom snake game environment
    '''
    # defines the render_mode parameter for the class
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode = None, speed = 15, width = 800, height = 800):
        '''
        INPUT: render_mode (Optional)
        OUTPUT: None

        Initialise the snake game environment
        Get the observation space and action space
        Check the render_mode of the environment
        '''
        self.width = width
        self.height = height
        self.speed = speed
        self.game = SnakeGameAI(self.width, self.height, self.speed)
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=np.array([0,0,0]), high=np.array([8,4,8]), dtype=np.int32)
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window = None
        self.clock = None

    def reset(self):
        '''
        INPUT: None
        OUTPUT: state

        Resets the game environment by deleting and reinitialising the game environment
        Gets the state of the environment
        Renders the game window if render_mode == "human"
        '''
        del self.game
        self.game = SnakeGameAI(self.width, self.height, self.speed)
        state = self.game.get_state(self.game)

        if self.render_mode == "human":
            self.game.draw_game()

        return state

    def step(self, action):
        '''
        INPUT: action
        OUTPUT: state, reward, done, truncated, score

        Gets the reward, done and score by running a gamestep
        Gets the new state of the environment
        Renders the game window if render_mode == "human"
        '''
        reward, done, score = self.game.game_step(action)
        state = self.game.get_state(self.game)

        if self.render_mode == "human":
            self.game.draw_game()

        return state, reward, done, False, {"Score": score}

    def render(self):
        '''
        Renders the game window if render_mode == "human"
        '''
        self.game.draw_game()

    def close(self):
        '''
        Closes the game environment
        '''
        pygame.display.quit()
        pygame.quit()

class CustomEnv_hard(gym.Env):
    '''
    This helps to initialise the custom snake game environment
    '''
    # defines the render_mode parameter for the class
    metadata = {'render_modes' : ['human']}

    def __init__(self, render_mode = None, speed = 15, width = 800, height = 800):
        '''
        INPUT: render_mode (Optional)
        OUTPUT: None

        Initialise the snake game environment
        Get the observation space and action space
        Check the render_mode of the environment
        '''
        self.width = width
        self.height = height
        self.speed = speed
        self.game = SnakeGameAI_hard(self.width, self.height, self.speed)
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=np.array([0,0,0]), high=np.array([8,4,8]), dtype=np.int32)
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window = None
        self.clock = None

    def reset(self):
        '''
        INPUT: None
        OUTPUT: state

        Resets the game environment by deleting and reinitialising the game environment
        Gets the state of the environment
        Renders the game window if render_mode == "human"
        '''
        del self.game
        self.game = SnakeGameAI_hard(self.width, self.height, self.speed)
        state = self.game.get_state(self.game)
        
        if self.render_mode == "human":
            self.game.draw_game()

        return state

    def step(self, action):
        '''
        INPUT: action
        OUTPUT: state, reward, done, truncated, score

        Gets the reward, done and score by running a gamestep
        Gets the new state of the environment
        Renders the game window if render_mode == "human"
        '''
        reward, done, score = self.game.game_step(action)
        state = self.game.get_state(self.game)
        
        if self.render_mode == "human":
            self.game.draw_game()

        return state, reward, done, False, {"Score": score}

    def render(self):
        '''
        Renders the game window if render_mode == "human"
        '''
        self.game.draw_game()

    def close(self):
        '''
        Closes the game environment
        '''
        pygame.display.quit()
        pygame.quit()