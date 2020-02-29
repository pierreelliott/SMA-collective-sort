import random
from random import randint
from collections import deque, Counter
from time import sleep
from GridGraphics import GridPG
from Agent import Agent
from Grid import Grid

random.seed(0)

# Environment constants
GRID_SIZE = 20
OBJECTS = (('A', 100), ('B', 100))
# Agents constants
NB_AGENTS = 50
MAX_MEMORY_SIZE = 10
NEIGHBOURHOOD_SIZE = 2
MAX_MOVES = 1
MAX_ITER = int(1e7)
K_PICK = 0.1  # k+
K_PUT = 0.3  # k-

REFRESH_FREQ = MAX_ITER // 10
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
        self.grid = Grid(grid_size, grid_size)
        # self.grid = [[None for i in range(grid_size)] for j in range(grid_size)]
        # self.agent_grid = [[None for i in range(grid_size)] for j in range(grid_size)]
        if PYGAME:
            self.grid_graphics = GridPG(grid_size, grid_size, objects)
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
            try:
                if self.grid.move(agent, move):
                    return
            except Exception:
                pass

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
                if PYGAME:
                    self.grid_graphics.draw_cell(j, i, cell.obj, cell.agent)
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
        if PYGAME:
            self.grid_graphics.display()
        if CONSOLE:
            print(''.join(s))


def init_agents(nb_agents: int, environment: Environment) -> [Agent]:
    agents = []
    for i in range(nb_agents):
        agents.append(Agent(environment))
    return agents


if __name__ == '__main__':
    env = Environment(objects=OBJECTS, grid_size=GRID_SIZE)
    agents = init_agents(NB_AGENTS, env)
    env.populate(agents)
    env.print_grids()
    sleep(1)
    for it in range(MAX_ITER):
        agent = random.choice(agents)
        agent.act()
        env.move(agent)
        if it % REFRESH_FREQ == 0:
            print(f"Iter {it}/{MAX_ITER}")
            env.print_grids()
