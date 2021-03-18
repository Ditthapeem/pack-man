import tkinter as tk
import random


from gamelib import Sprite, GameApp, Text

from dir_consts import *
from maze import Maze

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

UPDATE_DELAY = 33

PACMAN_SPEED = 5

class NormalPacmanState:
    def __init__(self, pacman):
        self.pacman = pacman

    def random_upgrade(self):
        if random.random() < 0.1:
            self.pacman.state = SuperPacmanState(self.pacman)

    def move_pacman(self):
        self.pacman.x += PACMAN_SPEED * DIR_OFFSET[self.pacman.direction][0]
        self.pacman.y += PACMAN_SPEED * DIR_OFFSET[self.pacman.direction][1]


class SuperPacmanState:
    def __init__(self, pacman):
        self.pacman = pacman
        self.counter = 0

    def random_upgrade(self):
        pass

    def move_pacman(self):
        self.pacman.x += PACMAN_SPEED *2* DIR_OFFSET[self.pacman.direction][0]
        self.pacman.y += PACMAN_SPEED *2* DIR_OFFSET[self.pacman.direction][1]
        self.counter +=1
        if self.counter >=100:
            self.pacman.state = NormalPacmanState(self.pacman)

class Pacman(Sprite):
    def __init__(self, app, maze, r, c):
        self.r = r
        self.c = c
        self.maze = maze

        self.direction = DIR_STILL
        self.next_direction = DIR_STILL

        x, y = maze.piece_center(r,c)
        super().__init__(app, 'images/pacman.png', x, y)

        self.state = NormalPacmanState(self)

    def update(self):
        if self.maze.is_at_center(self.x, self.y):
            r, c = self.maze.xy_to_rc(self.x, self.y)

            if self.maze.has_dot_at(r, c):
                self.maze.eat_dot_at(r, c)
                self.state.random_upgrade()

            
            if self.maze.is_movable_direction(r, c, self.next_direction):
                self.direction = self.next_direction
            else:
                self.direction = DIR_STILL

        self.state.move_pacman()


        # self.x += speed * DIR_OFFSET[self.direction][0]
        # self.y += speed * DIR_OFFSET[self.direction][1]

        # self.x += PACMAN_SPEED * DIR_OFFSET[self.direction][0]
        # self.y += PACMAN_SPEED * DIR_OFFSET[self.direction][1]

    def set_next_direction(self, direction):
        self.next_direction = direction


class PacmanGame(GameApp):
    def init_game(self):
        self.maze = Maze(self, CANVAS_WIDTH, CANVAS_HEIGHT)

        self.pacman1 = Pacman(self, self.maze, 1, 1)
        self.pacman2 = Pacman(self, self.maze, self.maze.get_height() - 2, self.maze.get_width() - 2)

        self.pacman1_score_text = Text(self, 'P1: 0', 100, 20)
        self.pacman2_score_text = Text(self, 'P2: 0', 600, 20)

        self.elements.append(self.pacman1)
        self.elements.append(self.pacman2)

        self.command_map = {
            'W': self.get_pacman_next_direction_function(self.pacman1, DIR_UP),
            'A': self.get_pacman_next_direction_function(self.pacman1, DIR_LEFT),
            'D': self.get_pacman_next_direction_function(self.pacman1, DIR_RIGHT),
            'S': self.get_pacman_next_direction_function(self.pacman1, DIR_DOWN),

            'I': self.get_pacman_next_direction_function(self.pacman2, DIR_UP),
            'J': self.get_pacman_next_direction_function(self.pacman2, DIR_LEFT),
            'L': self.get_pacman_next_direction_function(self.pacman2, DIR_RIGHT),
            'K': self.get_pacman_next_direction_function(self.pacman2, DIR_DOWN)

            # TODO:
            #   - add all other commands to the command_map
        }

    def pre_update(self):
        pass

    def get_pacman_next_direction_function(self, pacman, next_direction):

        def f():
            pacman.set_next_direction(next_direction)

        return f



    def post_update(self):
        pass

    def on_key_pressed(self, event):
        ch = event.char.upper()

        if ch in self.command_map:
            self.command_map[ch]()

        # if event.char.upper() == 'A':
        #     self.pacman1.set_next_direction(DIR_LEFT)
        # elif event.char.upper() == 'W':
        #     self.pacman1.set_next_direction(DIR_UP)
        # elif event.char.upper() == 'S':
        #     self.pacman1.set_next_direction(DIR_DOWN)
        # elif event.char.upper() == 'D':
        #     self.pacman1.set_next_direction(DIR_RIGHT)
        #
        # if event.char.upper() == 'J':
        #     self.pacman2.set_next_direction(DIR_LEFT)
        # elif event.char.upper() == 'I':
        #     self.pacman2.set_next_direction(DIR_UP)
        # elif event.char.upper() == 'K':
        #     self.pacman2.set_next_direction(DIR_DOWN)
        # elif event.char.upper() == 'L':
        #     self.pacman2.set_next_direction(DIR_RIGHT)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = PacmanGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
