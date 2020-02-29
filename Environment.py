from GridGraphics import GridPG
from Grid import Grid
from Agent import Agent
import random


class Environment:
    def __init__(self, objects: [(object, int)] = (('A', 200), ('B', 200)), grid_size: int = 50, pygame=False,
                 console=True):
        self.grid_size = grid_size

        self.PYGAME = pygame
        self.CONSOLE = console

        if self.PYGAME:
            self.grid = GridPG(grid_size, grid_size, objects)
        else:
            self.grid = Grid(grid_size, grid_size)

        for object_type, nb_object in objects:
            count = nb_object
            while count > 0:
                x, y = self.grid.get_random_empty_cell()
                self.grid.set_object((x, y), object_type)
                count -= 1

    def __repr__(self):
        self.grid.__repr__()

    def populate(self, agents: [Agent]):
        for agent in agents:
            x, y = self.grid.get_random_empty_cell()
            self.grid.set_agent((x, y), agent)

    def get_possible_moves(self, agent: Agent):
        M = agent.moves
        ranges = ((-M, 0), (M, 0), (0, -M), (0, M))
        possible_moves = []
        for r in ranges:
            possible_moves.append(tuple(item1 + item2 for item1, item2 in zip(agent.pos, r)))
        random.shuffle(possible_moves)
        return possible_moves

    def move(self, agent: Agent):
        moves = self.get_possible_moves(agent)
        for move in moves:
            if self.grid.move(agent, move):
                return

    def get_nb_objet_in_area(self, pos: tuple, obj_type: str):
        res = 0
        if pos[0] < self.grid_size - 1:
            c = (pos[0] + 1, pos[1])
            if self.get_obj(c) == obj_type:
                res += 1
        if pos[1] < self.grid_size - 1:
            c = (pos[0], pos[1] + 1)
            if self.get_obj(c) == obj_type:
                res += 1
        if pos[0] > 0:
            c = (pos[0] - 1, pos[1])
            if self.get_obj(c) == obj_type:
                res += 1
        if pos[1] > 0:
            c = (pos[0], pos[1] - 1)
            if self.get_obj(c) == obj_type:
                res += 1
        return res

    def get_obj(self, pos: tuple):
        return self.grid.get_object(pos)

    def set_obj(self, pos: tuple, obj):
        self.grid.set_object(pos, obj)

    def get_a(self, pos: tuple):
        return self.grid.get_agent(pos)

    def set_a(self, pos: tuple, a):
        self.grid.set_agent(pos, a)

    def print_grids(self):
        s = []
        for i, row in enumerate(self.grid.grid):
            for j, cell in enumerate(row):
                # if self.PYGAME:
                #     self.grid_graphics.draw_cell(j, i, cell.obj, cell.agent)
                if cell.agent is not None:
                    if cell.agent.carry:
                        s.append('§')
                    else:
                        s.append('+')
                if cell.obj is not None:
                    s.append(cell.obj)
                elif cell.agent is None:
                    s.append('.')
                s.append('\t')
            s.append('\n')
        if self.PYGAME:
            self.grid.display()
        if self.CONSOLE:
            print(''.join(s))
