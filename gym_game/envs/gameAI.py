####################################################
# Project: Snake Game                              #
# Author: Pranav Panchal                           #
# Date: 11/09/2022                                 # 
####################################################                               
# This is a snake game engine which take AI inputs #
####################################################

from collections import namedtuple
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
from IPython.display import clear_output

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

# game window variables
WIDTH = 800
HEIGHT = 800

BLOCK = 40
SPEED = 10000

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 105, 97)
GREEN = (119, 221, 119)
GRAY = (90, 102, 117)

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

Point = namedtuple("Point", "x, y")

clock = pygame.time.Clock()

class SnakeGameAI:
    # metadata = {"render_mode": ["human", "rgb_array"]}

    def __init__(self, WIDTH = 400, HEIGHT = 400):
        self.width = WIDTH
        self.height = HEIGHT

        # display event
        # self.WIN = pygame.display.set_mode((self.width, self.height))
        # pygame.display.set_caption("Snake AI!!!")
        
        # self.render_mode = render_mode
        self.clock = pygame.time.Clock()
        # self.n_games = 1
        # self.reset()

    # reset and re-initialise the game state
    # def reset(self):#, WIDTH, HEIGHT):    
        self.head = Point(self.width/2, self.height/2)
        self.snakebody = [self.head,
                          Point(self.head.x-BLOCK, self.head.y),
                          Point(self.head.x-(2*BLOCK), self.head.y)]
        self.direction = Direction.RIGHT
        self.score = 0
        self.gen_food()
        self.frame_iteration = 0
        # state = self.get_state(self)
        # display event
        # if self.render_mode == "human":
        # self.draw_game()
        #     self.render()
        # done = False
        # return state

    # generate food at a random location on map, if random location is within snakebody -> recall gen_food() again
    def gen_food(self):
        x = random.randint(0, (self.width - BLOCK) // BLOCK) * BLOCK
        y = random.randint(0, (self.width - BLOCK) // BLOCK) * BLOCK
        self.food = Point(x, y)
        if self.food in self.snakebody:
            self.gen_food()
        
    def game_step(self, action):
        # increase frame_iteration to run in-game clock
        self.frame_iteration += 1
                   
        # move in the current direction
        self.move(action)
        self.snakebody.insert(0, self.head)

        # state = self.get_state(self)

        # checks whether game is done(over)
        reward = 0
        done = False
        if self.is_collision():# or self.frame_iteration > 100 * len(self.snakebody):
            reward = -10
            done = True
            return reward, done, self.score

        # check new step resulted in eating food (YES -> increase score, get reward, gen_food()) |#| (NO -> move and shift the tail)
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.frame_iteration = 0
            self.gen_food()
        else:
            self.snakebody.pop()        

        # display event
        # if self.render_mode == "human":
        # self.draw_game()
        #     self.render()

        self.clock.tick(SPEED)

        return reward, done, self.score
    
    def move(self, action):
        clockwise = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        idx = clockwise.index(self.direction)

        if action == 0: # action == [0,1,0]
            self.direction = clockwise[idx]
        elif action == 1: # action == [1,0,0]
            self.direction = clockwise[(idx - 1) % 4]
        elif action == 2: # action == [0,0,1]
            self.direction = clockwise[(idx + 1) % 4]

        # self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK
        elif self.direction == Direction.LEFT:
            x -= BLOCK
        elif self.direction == Direction.UP:
            # print(new_direction)
            y -= BLOCK
        elif self.direction == Direction.DOWN:
            y += BLOCK

        self.head = Point(x, y)
        return self.head

    def is_collision(self, pt = None):
        if pt is None:
            pt = self.head
        if pt.x < 0 or pt.x > self.width - BLOCK or pt.y < 0 or pt.y > self.height - BLOCK:
            return True
        elif self.head in self.snakebody[1:]:
            return True          


    def draw_game(self):
        self.WIN = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake AI!!!")

        self.WIN.fill(BLACK)

        self.clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        for x in np.arange(BLOCK, WIDTH, BLOCK):
            pygame.draw.line(self.WIN, GRAY, (x, 0), (x, HEIGHT))
        for y in np.arange(BLOCK, HEIGHT, BLOCK):
            pygame.draw.line(self.WIN, GRAY, (0, y), (WIDTH, y))

        for item in self.snakebody:
            pygame.draw.rect(self.WIN, RED, (item.x, item.y, BLOCK, BLOCK))

        # display food
        pygame.draw.rect(self.WIN, GREEN, (self.food.x, self.food.y, BLOCK, BLOCK))

        # display score
        pygame.font.init()
        font = pygame.font.Font('arial.ttf', (BLOCK - 2))
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.WIN.blit(text, [0, 0])
        pygame.display.flip()

    def get_state(self, game):
        head = game.snakebody[0]
        head_l = Point(head.x - BLOCK, head.y)
        head_r = Point(head.x + BLOCK, head.y)
        head_u = Point(head.x, head.y - BLOCK)
        head_d = Point(head.x, head.y + BLOCK)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        dan = [
            # Danger straight
            (dir_r and game.is_collision(head_r)) or 
            (dir_l and game.is_collision(head_l)) or 
            (dir_u and game.is_collision(head_u)) or 
            (dir_d and game.is_collision(head_d)),

            # Danger right
            (dir_r and game.is_collision(head_d)) or 
            (dir_l and game.is_collision(head_u)) or 
            (dir_u and game.is_collision(head_r)) or 
            (dir_d and game.is_collision(head_l)),

            # Danger left
            (dir_r and game.is_collision(head_u)) or 
            (dir_l and game.is_collision(head_d)) or 
            (dir_u and game.is_collision(head_l)) or 
            (dir_d and game.is_collision(head_r))
        ]

        direc = [
            # Move direction
            dir_r,
            dir_l,
            dir_u,
            dir_d,
        ]

        apple = [
            # Food location
            game.food.y < game.head.y,  # food up
            game.food.x > game.head.x,  # food right
            game.food.y > game.head.y,  # food down
            game.food.x < game.head.x,  # food left
        ]

        for i, v in enumerate(dan):
            if v == None:
                dan[i] = 0

        dan_list = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]

        for i, v in enumerate(dan_list):
            if dan == v:
                dan = i

        direc_list = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]

        for i, v in enumerate(direc_list):
            if direc == v:
                direc = i
        
        apple_list = [[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0],[1,0,0,0],[1,0,0,1]]

        for i, v in enumerate(apple_list):
            if apple == v:
                apple = i

        state = (dan,direc,apple)

        return state

    # def get_action(self):#, state):
    #     move = random.randint(0, 2)
                
    #     return move

def main():
    s = SnakeGameAI()
    for i in range(10):        
        # clear_output(wait = True)
        st = s.get_state(s)
        print(st)
        print(type(st))
        a = s.get_action()       
        reward, done, score = s.game_step(a)
        s.clock.tick(SPEED)
        # if done:
        #     break

if __name__ == "__main__":
    main()