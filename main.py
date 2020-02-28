import random
from random import randint
from collections import deque, Counter
from time import sleep

random.seed(0)

# Environment constants
GRID_SIZE = 50
OBJECTS = (('A', 200), ('B', 200))
# Agents constants
NB_AGENTS = 20
MAX_MEMORY_SIZE = 10
NEIGHBOURHOOD_SIZE = 2
MAX_MOVES = 1
MAX_ITER = 10000
K_PICK = 0.1    # k+
K_PUT = 0.3     # k-

REFRESH_FREQ = 1000


# ===================== Helpers =======================
def random_position_in_grid(grid_size: int):
    x = randint(0, grid_size - 1)
    y = randint(0, grid_size - 1)
    return x, y


def create_manhattan_distance(position: (int, int)):
    return lambda x, y: abs(x - position[0]) + abs(y - position[1])
# ====================================================


class Agent:
    def __init__(self, environment, moves: int = 1):
        self.memory = deque(maxlen=MAX_MEMORY_SIZE)  # FIXME Give it as a parameter ?
        self.carry = None  # What is the agent currently carrying
        self.moves = moves  # Number of moves (ie, move 1 cell in any direction) the agent can do
        self.env = environment
        self.pos = None

    def memorize(self, element: object):
        self.memory.append(element)

    def act(self):
        # Perception
        o = env.get_obj(self.pos)
        self.memory.append(o)

        # Try pick up
        if o is not None and self.p_pick(o) > random.random():
            self.carry = o
            self.env.set_obj(self.pos, None)
        # Try put down
        elif self.carry and self.p_put(o) > random.random():
            self.carry = None
            self.env.set_obj(self.pos, o)

    def p_pick(self, obj_type: str):
        f = env.get_nb_objet_in_area(self.pos, obj_type)
        return (K_PICK / (K_PICK + f)) ** 2

    def p_put(self, obj_type: str):
        f = env.get_nb_objet_in_area(self.pos, obj_type)
        return (f / (K_PUT + f)) ** 2


class Environment:
    def __init__(self, objects: [(object, int)] = (('A', 200), ('B', 200)), grid_size: int = 50):
        self.grid_size = grid_size
        self.grid = [[None for i in range(grid_size)] for j in range(grid_size)]
        self.agent_grid = [[None for i in range(grid_size)] for j in range(grid_size)]
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
            self.agent_grid[position[0]][position[1]] = agent
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

    def print_grids(self):
        s = []
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                agent = self.get_a((i, j))
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
    for it in range(MAX_ITER):
        sleep(0.5)
        agent = random.choice(agents)
        agent.act()
        env.move(agent)
        if it % REFRESH_FREQ == 0:
            env.print_grids()
