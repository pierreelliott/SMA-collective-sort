import random
from random import randint
from collections import deque, Counter

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


# ===================== Helpers =======================
def random_position_in_grid(grid_size: int):
    x = randint(0, grid_size - 1)
    y = randint(0, grid_size - 1)
    return x, y


def create_manhattan_distance(position: (int, int)):
    return lambda x, y: abs(x - position[0]) + abs(y - position[1])
# ====================================================


class Agent:
    def __init__(self, environment, pos, moves: int = 1):
        self.memory = deque(maxlen=MAX_MEMORY_SIZE)  # FIXME Give it as a parameter ?
        self.carry = None  # What is the agent currently carrying
        self.moves = moves  # Number of moves (ie, move 1 cell in any direction) the agent can do
        self.env = environment
        self.pos = None

    def memorize(self, element: object):
        self.memory.append(element)

    def act(self):
        # Perception
        current_cell = self.env.grid[self.pos[0]][self.pos[1]]
        self.memory.append(current_cell)

        # Act
        if current_cell is not None:
            # Try put down
            if self.carry:
                pass
            # Try pick up
            else:
                pass


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

    def move(self, agent: Agent):
        possible_range = list(range(-agent.moves, agent.moves))     # (-2, -1, 0, 1, 2) for moves = 2
        possible_range.remove(0)

        position = agent.pos[:]
        position[0] += random.choice(possible_range)
        position[1] += random.choice(possible_range)

        if 0 <= position[0] < self.grid_size and 0 <= position[1] < self.grid_size \
                and self.grid[position[0]][position[1]] is None:
            self.grid[position[0]][position[1]] = agent
            agent.pos = position


def init_agents(nb_agents: int, environment: Environment) -> [Agent]:
    agents = []
    for i in range(nb_agents):
        agents.append(Agent(environment))
    return agents


if __name__ == '__main__':
    env = Environment(objects=OBJECTS, grid_size=GRID_SIZE)
    agents = init_agents(NB_AGENTS, env)
    env.populate(agents)
    for it in range(MAX_ITER):
        agent = random.choice(agents)
        agent.act()
        env.move(agent)
