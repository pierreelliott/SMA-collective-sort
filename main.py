import random
from random import randint
from time import sleep
from Agent import Agent
from Environment import Environment

random.seed(0)

# Environment constants
GRID_SIZE = 20
OBJECTS = (('A', 100), ('B', 100))
# Agents constants
NB_AGENTS = 50
MAX_MEMORY_SIZE = 10
NEIGHBOURHOOD_SIZE = 2
MOVES = 1
MAX_ITER = int(1e7)
K_PICK = 0.1  # k+
K_PUT = 0.3  # k-
RECOGNITION_ERROR = 0.2
# RECOGNITION_ERROR = 0

# REFRESH_FREQ = MAX_ITER // 1000
REFRESH_FREQ = 1000
LOOK_AROUND = False

PYGAME = True
CONSOLE = False
VERBOSE = False


# ===================== Helpers =======================
def random_position_in_grid(grid_size: int):
    x = randint(0, grid_size - 1)
    y = randint(0, grid_size - 1)
    return x, y


def create_manhattan_distance(position: (int, int)):
    return lambda x, y: abs(x - position[0]) + abs(y - position[1])


# ====================================================


def init_agents(nb_agents: int, environment: Environment) -> [Agent]:
    agents = []
    for i in range(nb_agents):
        agents.append(Agent(environment, moves=MOVES, recognition_error=RECOGNITION_ERROR, k_pick=K_PICK,
                            k_put=K_PUT))
    return agents


if __name__ == '__main__':
    env = Environment(objects=OBJECTS, grid_size=GRID_SIZE, pygame=PYGAME, console=CONSOLE)
    agents = init_agents(NB_AGENTS, env)
    env.populate(agents)
    env.print_grids()
    sleep(1)
    for it in range(MAX_ITER):
        agent = random.choice(agents)
        agent.act()
        env.move(agent)
        if it % REFRESH_FREQ == 0:
            if VERBOSE:
                print(f"Iter {it}/{MAX_ITER}")
            env.print_grids()
