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


# ===================== Helpers =======================
def random_position_in_grid(grid_size: int):
    x = randint(0, grid_size - 1)
    y = randint(0, grid_size - 1)
    return x, y


def create_manhattan_distance(position: (int, int)):
    return lambda x, y: abs(x - position[0]) + abs(y - position[1])
# ====================================================


class Agent:
    def __init__(self, neighbourhood_size: int, moves: int = 1):
        self.memory = deque(maxlen=MAX_MEMORY_SIZE)  # FIXME Give it as a parameter ?
        self.carry = None  # What is the agent currently carrying
        self.moves = moves  # Number of moves (ie, move 1 cell in any direction) the agent can do
        self.neighbourhood_size = neighbourhood_size

    def memorize(self, most_frequent_elem_in_area: object):
        self.memory.append(most_frequent_elem_in_area)

    def act(self):
        return self.carry is not None


class Environment:
    def __init__(self, objects: [(object, int)] = (('A', 200), ('B', 200)), grid_size: int = 50):
        self.grid_size = grid_size
        self.grid = [[None for i in range(grid_size)] for j in range(grid_size)]
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
                if self.grid[y][x] is None:
                    self.grid[y][x] = agent

    def perception(self, agent: Agent):
        # Find agent
        for y, line in enumerate(self.grid):
            if agent in line:
                x = line.index(agent)
                break
        # Find most frequent element in the neighbourhood
        most_frequent = self._most_frequent_in_area(agent, (x, y))
        # Memorize it
        agent.memorize(most_frequent)

    def _most_frequent_in_area(self, agent: Agent, position: (int, int)) -> object:
        dist = create_manhattan_distance(position)
        area = []
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell is not None and dist(x, y) < agent.neighbourhood_size:
                    area.append(cell)
        return Counter(area).most_common(1)[0][0]

    def move(self, agent: Agent):
        # TODO
        pass


def init_agents(nb_agents: int) -> [Agent]:
    agents = []
    for i in range(nb_agents):
        agents.append(Agent(NEIGHBOURHOOD_SIZE))
    return agents


def main_loop():
    env = Environment(objects=OBJECTS, grid_size=GRID_SIZE)
    agents = init_agents(NB_AGENTS)
    env.populate(agents)
    sorted = False
    while not sorted:
        agent = random.choice(agents)
        env.perception(agent)

        if not agent.carry:
            # Try to pick something
            pass

        if agent.carry:
            # Try to put something down
            pass

        env.move(agent)
