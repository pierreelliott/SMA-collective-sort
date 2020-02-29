from random import randint


class Grid:
    def __init__(self, rows, columns):
        self.grid = [[Cell((i, j)) for i in range(columns)] for j in range(rows)]
        self.ROW_SIZE = rows
        self.COL_SIZE = columns

    def get(self, pos: (int, int)):
        """

        :param pos: Position in the grid as (x, y)
        :return:
        """
        x, y = pos
        if x < 0 or y < 0 or x >= self.COL_SIZE or y >= self.ROW_SIZE:
            raise Exception("Out of range")
        return self.grid[y][x]

    def set(self, pos: (int, int), obj: object):
        """

        :param obj:
        :param pos: Position in the grid as (x, y)
        :return:
        """
        x, y = pos
        if x < 0 or y < 0 or x >= self.COL_SIZE or y >= self.ROW_SIZE:
            raise Exception("Out of range")
        self.grid[y][x] = obj

    def for_each_cell(self, func):
        for y in range(self.ROW_SIZE):
            for x in range(self.COL_SIZE):
                func(self.get((x, y)))

    def get_random_empty_cell(self):
        cell_found = False
        x, y = 0, 0
        # cell = Cell((x, y))
        while not cell_found:
            x = randint(0, self.COL_SIZE - 1)
            y = randint(0, self.ROW_SIZE - 1)
            cell = self.get((x, y))
            cell_found = cell.empty()
        return x, y

    def __repr__(self):
        # Print the grid
        for i in range(self.ROW_SIZE):
            for j in range(self.COL_SIZE):
                print(self.grid[i][j], end=" ")
            print()

    def move(self, agent, pos: (int, int)):
        try:
            available = self.get(pos).available()
        except:
            return False
        if available:
            self.set_agent(agent.pos, None)
            self.set_agent(pos, agent)
            return True
        else:
            return False

    def set_object(self, pos: (int, int), obj: object):
        self.get(pos).obj = obj

    def get_object(self, pos: (int, int)):
        return self.get(pos).obj

    def set_agent(self, pos: (int, int), agent):
        self.get(pos).agent = agent
        if agent is not None:
            agent.pos = pos

    def get_agent(self, pos: (int, int)):
        return self.get(pos).agent


class Cell:
    def __init__(self, pos: (int, int)):
        self.agent = None
        self.obj = None
        self.pos = pos

    def empty(self):
        return not self.obj and self.available()

    def available(self):
        return not self.agent
