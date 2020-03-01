import random
from random import randint
from time import sleep, time
from Agent import Agent
from Environment import Environment
from pynput.keyboard import Key, Listener, KeyCode

# ============================================================================
# =============================== PARAMETERS =================================
# Environment constants
GRID_SIZE_X = 50
GRID_SIZE_Y = 50
OBJECTS = (('A', 200), ('B', 200))
# Agents constants
NB_AGENTS = 50
MAX_MEMORY_SIZE = 10
MOVES = 1  # i (ie, neighborhood)
MAX_ITER = int(1e7)
K_PICK = 0.1  # k+
K_PUT = 0.3  # k-
RECOGNITION_ERROR = 0
# RECOGNITION_ERROR = 0


PYGAME = True  # Display the Pygame graphics
CONSOLE = False  # Print the grid in the console for every iteration
VERBOSE = False  # Shox iteration count in the console

# ============================================================================
# ============================================================================

# REFRESH_FREQ = MAX_ITER // 1000
REFRESH_FREQ = 1000
LOOK_AROUND = False  # Not used
RANDOM_AGENT = True  # Pick an agent whom will act at random (or pick each agent in round robin)

# Runtime Vars
PAUSE = False
STOP = False

random.seed(0)


# ===================== Helpers =======================
def print_helper_commands():
    print("Commandes de la simulation :")
    print("I : Afficher les commandes de la simulation (ie, ceci)")
    print("Q : Quitter la simulation")
    print("Espace : Mettre en pause la simulation")
    print("↑ (Flèche Haut) : Augmenter la vitesse de la simulation")
    print("↓ (Flèche Bas) : Diminuer la vitesse de la simulation")
    print("=========================")
    print()


def on_press(key):
    global PAUSE
    global REFRESH_FREQ
    global STOP
    if key == Key.space:
        PAUSE = not PAUSE
    elif key == Key.up:
        REFRESH_FREQ = min(1e6, REFRESH_FREQ * 10)
    elif key == Key.down:
        REFRESH_FREQ = max(1, int(REFRESH_FREQ / 10))
    elif key == KeyCode(char="q"):
        STOP = True
    elif key == KeyCode(char="i"):
        print_helper_commands()
    # elif key == KeyCode(char="a"):
    #     grid.show_agent = not grid.show_agent
    #     # print(GRID_BORDER, end="\r")
    # elif key == KeyCode(char="b"):
    #     grid.show_border = not grid.show_border
    #     # print(GRID_UPDATE)
    # for i in range(len(GRID_UPDATES)):
    #     kc = KeyCode(char=str(i))
    #     if key == kc:
    #         GRID_UPDATE[0] = GRID_UPDATES[i]
    #         print(GRID_UPDATE)


def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False


# ====================================================
i_agent = 0


def pick_agent(agents):
    if RANDOM_AGENT:
        return random.choice(agents)
    else:
        global i_agent
        a = agents[i_agent]
        i_agent = (i_agent + 1)%len(agents)
        return a


def init_agents(nb_agents: int, environment: Environment) -> [Agent]:
    agents = []
    for i in range(nb_agents):
        agents.append(Agent(environment, moves=MOVES, recognition_error=RECOGNITION_ERROR, k_pick=K_PICK,
                            k_put=K_PUT, mem_size=MAX_MEMORY_SIZE))
    return agents


if __name__ == '__main__':
    starting_time = time()
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    print_helper_commands()
    env = Environment(objects=OBJECTS, grid_size=(GRID_SIZE_Y, GRID_SIZE_X), pygame=PYGAME, console=CONSOLE)
    agents = init_agents(NB_AGENTS, env)
    env.populate(agents)
    env.print_grids()
    sleep(1)
    for it in range(MAX_ITER):
        if PAUSE:
            print("PAUSE")
            print(f"Current iteration {it}/{MAX_ITER}")
        while PAUSE:
            pass

        agent = pick_agent(agents)
        env.move(agent)
        agent.act()
        if it % REFRESH_FREQ == 0:
            if VERBOSE:
                print(f"Iter {it}/{MAX_ITER}")
            env.print_grids()

        if STOP:
            print("=========================")
            print(f"Iteration {it} on {MAX_ITER} (max)")
            print(f"Sort done in {time() - starting_time:.2f} seconds")
            break
