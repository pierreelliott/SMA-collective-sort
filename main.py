import random
from random import randint
from collections import deque, Counter
from time import sleep
from GridGraphics import GridPG
from Agent import Agent

random.seed(0)

# Environment constants
GRID_SIZE = 50
OBJECTS = (('A', 200), ('B', 200))
# Agents constants
NB_AGENTS = 50
MAX_MEMORY_SIZE = 10
NEIGHBOURHOOD_SIZE = 2
MAX_MOVES = 1
MAX_ITER = int(1e7)
K_PICK = 0.1    # k+
K_PUT = 0.3     # k-

REFRESH_FREQ = MAX_ITER//10
# REFRESH_FREQ = 10
LOOK_AROUND = False

PYGAME = False
CONSOLE = True


# ===================== Helpers =======================
def random_position_in_grid(grid_size: int):
    x = randint(0, grid_size - 1)
    y = randint(0, grid_size - 1)
    return x, y


def create_manhattan_distance(position: (int, int)):
    return lambda x, y: abs(x - position[0]) + abs(y - position[1])
# ====================================================


class Environment:
    def __init__(self, objects: [(object, int)] = (('A', 200), ('B', 200)), grid_size: int = 50):
        self.grid_size = grid_size
        self.grid = [[None for i in range(grid_size)] for j in range(grid_size)]
        self.agent_grid = [[None for i in range(grid_size)] for j in range(grid_size)]
        if PYGAME:
            self.grid_graphics = GridPG(grid_size, grid_size, objects)
        for object_type, nb_object in objects:
            count = nb_object
            while count > 0:
                x, y = random_position_in_grid(grid_size)
                if self.grid[y][x] is None:
                    self.grid[y][x] = object_type
                    count -= 1

    def __repr__(self):
        # Print the grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                print(self.grid[i][j], end=" ")
            print()

    def populate(self, agents: [Agent]):
        for agent in agents:
            placed = False
            while not placed:
                x, y = random_position_in_grid(self.grid_size)
                if self.agent_grid[y][x] is None:
                    self.agent_grid[y][x] = agent
                    agent.pos = (y, x)
                    placed = True

    def move(self, agent: Agent):
        possible_range = list(range(-agent.moves, agent.moves+1))     # (-2, -1, 0, 1, 2) for moves = 2
        possible_range.remove(0)

        x = agent.pos[0] + random.choice(possible_range)
        y = agent.pos[1] + random.choice(possible_range)
        position = (x, y)

        if 0 <= position[0] < self.grid_size and 0 <= position[1] < self.grid_size and self.get_a(position) is None:
            self.set_a(agent.pos, None)
            self.set_a(position, agent)
            agent.pos = position

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
        return self.grid[pos[0]][pos[1]]

    def set_obj(self, pos: tuple, obj):
        self.grid[pos[0]][pos[1]] = obj

    def get_a(self, pos: tuple):
        return self.agent_grid[pos[0]][pos[1]]

    def set_a(self, pos: tuple, a):
        self.agent_grid[pos[0]][pos[1]] = a

    def print_grids(self):
        s = []
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                agent = self.get_a((i, j))
                if PYGAME:
                    self.grid_graphics.draw_cell(j, i, cell, agent)
                if agent is not None:
                    if agent.carry:
                        s.append('§')
                    else:
                        s.append('+')
                if cell is not None:
                    s.append(cell)
                elif agent is None:
                    s.append('.')
                s.append('\t')
            s.append('\n')
        if PYGAME:
            self.grid_graphics.display()
        if CONSOLE:
            print(''.join(s))


def init_agents(nb_agents: int, environment: Environment) -> [Agent]:
    agents = []
    for i in range(nb_agents):
        agents.append(Agent(environment))
    return agents


def count_obj(env):
    count = 0
    for row in env.grid:
        for cell in row:
            if cell:
                count += 1
    for row in env.agent_grid:
        for cell in row:
            if cell and cell.carry:
                count += 1
    return count


if __name__ == '__main__':
    env = Environment(objects=OBJECTS, grid_size=GRID_SIZE)
    agents = init_agents(NB_AGENTS, env)
    env.populate(agents)
    env.print_grids()
    for it in range(MAX_ITER):
    # for it in range(10000):
        agent = random.choice(agents)
        agent.act()
        env.move(agent)
        if it % REFRESH_FREQ == 0:
            print(f"Iter {it}/{MAX_ITER}")
            env.print_grids()
