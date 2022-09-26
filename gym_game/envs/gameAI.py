####################################################
# Project: Snake Game                              #
# Author: Pranav Panchal                           #
# Date: 11/09/2022                                 # 
####################################################                               
# This is a snake game engine which take AI inputs #
####################################################

# Importing dependencies
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
BLOCK = 40

# game colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 105, 97)
GREEN = (119, 221, 119)
GRAY = (90, 102, 117)

class Direction(Enum):
    '''
    This maps the direction variables to numbers
    '''
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

# create a namedtuple
Point = namedtuple("Point", "x, y")

class SnakeGameAI:
    '''
    This class defines the snake game environment
    '''

    def __init__(self, WIDTH, HEIGHT, SPEED):
        '''
        Initialises the snake game environment.
        Reads the game HEIGHT and game WIDTH passed while calling the class and overwrites it on the default
        Initialises the game clock
        Initialises the snake head and body
        Give the snake a direction to move in
        Sets the game score to 0
        Spawns the food
        '''
        self.width = WIDTH
        self.height = HEIGHT
        self.speed = SPEED
        self.clock = pygame.time.Clock()   
        self.head = Point(((self.width/BLOCK)//2)*BLOCK, ((self.height/BLOCK)//2)*BLOCK)
        self.snakebody = [self.head,
                          Point(self.head.x-BLOCK, self.head.y),
                          Point(self.head.x-(2*BLOCK), self.head.y)]
        self.direction = Direction.RIGHT
        self.score = 0
        self.gen_food()

    def gen_food(self):
        '''
        Picks a random location on the grid and places the food there
        If random location is within snakebody -> recall gen_food()
        '''
        x = random.randint(0, (self.width - BLOCK) // BLOCK) * BLOCK
        y = random.randint(0, (self.height - BLOCK) // BLOCK) * BLOCK
        self.food = Point(x, y)
        if self.food in self.snakebody:
            self.gen_food()
        
    def game_step(self, action):
        '''
        INPUT: action
        OUTPUT: reward, done, score

        Takes a single gamestep lasting 1 game time unit

        First it moves the snake by reading the 'action' passed to function move
        Set game reward to 0 and sets 'done' to False
        Checks for collision
        Checks whether movement caused the snake to eat food or not
        '''                   
        # move in the current direction
        self.move(action)
        self.snakebody.insert(0, self.head)

        # check whether game is done(over)
        # YES -> decrease reward by 10, make done = TRUE
        # NO -> do nothing
        reward = 0
        done = False
        if self.is_collision():
            reward = -10
            done = True
            return reward, done, self.score

        # check new step resulted in eating food 
        # YES -> increase score, get reward, gen_food()
        # NO -> move and shift the tail
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.gen_food()
        else:
            self.snakebody.pop()        

        self.clock.tick(self.speed)

        return reward, done, self.score
    
    def move(self, action):
        '''
        INPUT: action
        OUTPUT: new position of head of snake

        Accepts the action passed to the function, reads it and determines the direction change, if any
        Move the snake head in that direction by 1 BLOCK
        '''
        clockwise = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        idx = clockwise.index(self.direction)

        # check if the action caused the snake to change its direction
        if action == 0: # action == [0,1,0] -> Go Straight
            self.direction = clockwise[idx]
        elif action == 1: # action == [1,0,0] -> Turn Left
            self.direction = clockwise[(idx - 1) % 4]
        elif action == 2: # action == [0,0,1] -> Turn Right
            self.direction = clockwise[(idx + 1) % 4]

        # move the snake by 1 block in the direction it is facing
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK
        elif self.direction == Direction.LEFT:
            x -= BLOCK
        elif self.direction == Direction.UP:
            y -= BLOCK
        elif self.direction == Direction.DOWN:
            y += BLOCK
        
        self.head = Point(x, y)

        return self.head

    def is_collision(self, pt = None):
        '''
        INPUT: a point on game grid -> (Optional)
        OUTPUT: bool
        
        Check whether the snake movement resulted in a collision with wall or snakebody
        
        If a separate point is passed as an argument, then it checks whether that point results in a collision
        If no point is passed, it check whether snake head has collided
        '''
        # Check the 'x' and 'y' location of the snake head and determine 
        # whether it has collided with a wall or its own body
        if pt is None:
            pt = self.head
        if pt.x < 0 or pt.x > self.width - BLOCK or pt.y < 0 or pt.y > self.height - BLOCK:
            return True
        elif self.head in self.snakebody[1:]:
            return True          


    def draw_game(self):
        '''
        Initialises the visual elements of the snake game like the game window, snake body etc.
        '''
        # initialise the game window and set caption
        self.WIN = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake AI!!!")

        # fill the game window with a background color
        self.WIN.fill(BLACK)

        # check for the event of closing the game window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # display the grid lines
        for x in np.arange(BLOCK, self.width, BLOCK):
            pygame.draw.line(self.WIN, GRAY, (x, 0), (x, self.height))
        for y in np.arange(BLOCK, self.height, BLOCK):
            pygame.draw.line(self.WIN, GRAY, (0, y), (self.width, y))
        
        # display snakebody
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
        '''
        INPUT: game
        OUTPUT: state

        This function returns the current state of the game encoded as tuple containing 3 integers

        Example outputs:
        (8, 2, 3)
        (4, 3, 7)
        '''
        # locates the head of the snake and creates points 1 BLOCK distance away from snake head in all directions
        head = game.snakebody[0]
        head_l = Point(head.x - BLOCK, head.y)
        head_r = Point(head.x + BLOCK, head.y)
        head_u = Point(head.x, head.y - BLOCK)
        head_d = Point(head.x, head.y + BLOCK)
        
        # gets the direction of snake head movement and converts it into a boolean variable
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        # checks whether the front, left or right points just created results in collision of not
        # and creates a list of 3 bool values depicting the danger blocks around the snake head
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

        # creates a list of 4 bool values depicting the snake head movement direction
        direc = [
            # Move direction
            dir_r,
            dir_l,
            dir_u,
            dir_d,
        ]

        # check the relative location of food w.r.t. to snake head
        apple = [
            # Food location
            game.food.y < game.head.y,  # food up
            game.food.x > game.head.x,  # food right
            game.food.y > game.head.y,  # food down
            game.food.x < game.head.x,  # food left
        ]

        # fixes an issue when sometime the boolean function for checking collision return a 'None' value
        for i, v in enumerate(dan):
            if v == None:
                dan[i] = 0

        # list of all possible danger values on the game grid and mapping them to integers
        dan_list = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
        for i, v in enumerate(dan_list):
            if dan == v:
                dan = i
        
        # list of all possible direction on the game grid and mapping them to integers
        direc_list = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]
        for i, v in enumerate(direc_list):
            if direc == v:
                direc = i
        
        # list of all possible food locations on the game grid and mapping them to integers
        apple_list = [[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0],[1,0,0,0],[1,0,0,1]]
        for i, v in enumerate(apple_list):
            if apple == v:
                apple = i

        # getting a tuple out of the integer values
        state = (dan,direc,apple)

        return state