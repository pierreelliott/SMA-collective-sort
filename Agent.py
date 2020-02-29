from collections import deque
import random

AGENT_ID = 0


class Agent:
    def __init__(self, environment, moves: int = 1, recognition_error: float = 0, mem_size: int = 10,
                 look_around=False, k_pick=0.1, k_put=0.3):
        global AGENT_ID
        AGENT_ID += 1
        self.id = AGENT_ID
        self.recognition_error = recognition_error
        self.memory = deque(maxlen=mem_size)
        self.carry = None  # What is the agent currently carrying
        self.moves = moves  # Number of moves (ie, move 1 cell in any direction) the agent can do
        self.env = environment
        self.pos = None
        self.LOOK_AROUND = look_around
        self.K_PICK = k_pick
        self.K_PUT = k_put

    def memorize(self, element: object):
        self.memory.append(element)

    def act(self):
        # Perception on current cell
        o = self.env.get_obj(self.pos)
        self.memorize(o)

        # Try pick up
        if not self.carry and o is not None and self.p_pick(o) > random.random():
            self.carry = o
            self.env.set_obj(self.pos, None)  # Remove object from grid
        # Try put down
        elif self.carry and o is None and self.p_put(self.carry) > random.random():
            self.env.set_obj(self.pos, self.carry)
            self.carry = None

    def f_mem(self, object_type: str):
        nb_type = self.memory.count(object_type)
        nb_others = len(self.memory) - nb_type
        f_ = nb_type
        if self.recognition_error:
            f_ += self.recognition_error * nb_others
        return f_ / len(self.memory)

    def f_grid(self, object_type: str):
        # Count object in specific area around the agent
        nb_type = self.env.get_nb_objet_in_area(self.pos, object_type)
        return 0  # TODO

    def f(self, object_type: str):
        f = self.f_mem(object_type)
        if self.LOOK_AROUND:
            f += self.f_grid(object_type)
        return f

    def p_pick(self, obj_type: str):
        """
        Probabilité de ramasser l'objet sur la case courante

        :param obj_type:
        :return:
        """
        f = self.f(obj_type)
        return (self.K_PICK / (self.K_PICK + f)) ** 2

    def p_put(self, obj_type: str):
        """
        Probabilité de déposer l'objet sur la case courante

        :param obj_type:
        :return:
        """
        f = self.f(obj_type)
        return (f / (self.K_PUT + f)) ** 2