import pygame as pg
from colour import Color
from Grid import Grid
import time


WINDOW_SIZE_X = 600
WINDOW_SIZE_Y = 600

# TILE_BORDER_SIZE = 0
TILE_BORDER_SIZE = 1

COLORS = (Color("green"), Color("red"), Color("blue"), Color("brown"))
HOLDING_COLORS = (Color("lightgreen"), Color("salmon"), Color("cyan"), Color("orange"))
FONT_COLOR = Color("black")
FONT_SIZE = 10
AGENT_COLOR = Color("gold")

# DISPLAY_TIME = 0
DISPLAY_TIME = 0.01
# DISPLAY_TIME = 0.1
# DISPLAY_TIME = 0.5
# DISPLAY_TIME = 1


class GridPG(Grid):
    def __init__(self, rows, columns, objects, show_border=False, show_agent=True):
        super().__init__(rows, columns)
        self.show_agent = show_agent
        self.show_border = show_border
        self.square_size_x = WINDOW_SIZE_X/columns  # columns
        self.square_size_y = WINDOW_SIZE_Y/rows  # lines
        print(self.square_size_x, self.square_size_y)
        pg.init()
        pg.font.init()

        self.objects_color = dict()
        self.holder_color = dict()
        i = 0
        for obj_type, _ in objects:
            self.objects_color[obj_type] = self.edit_color(COLORS[i])
            self.holder_color[obj_type] = self.edit_color(HOLDING_COLORS[i])
            i += 1

        self.color_agent = self.edit_color(AGENT_COLOR)
        self.color_font = self.edit_color(FONT_COLOR)

        self.font = pg.font.Font(
            pg.font.get_default_font(), FONT_SIZE)
        self.gameDisplay = pg.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
        pg.display.set_caption("SMA - Collective Sort")
        self.for_each_cell(self.draw_cell)
        pg.display.update()

    def draw_cell(self, cell):
        # color = Color(rgb=(random(), random(), random()))
        color = self.edit_color(Color("white"))
        object_cell = None
        text = ""

        if cell.obj is not None:
            # There is an object to draw
            color = self.objects_color[cell.obj]
        # else:
        #     print("Problème !")
        if cell.agent is not None:
            # Draw agent
            if cell.agent.carry:
                color = self.holder_color[cell.agent.carry]
            else:
                color = self.color_agent
            text = str(cell.agent.id)

        self.draw_tile(cell.pos[0], cell.pos[1], color=color, text=text)

    def draw_tile(self, col, line, color=Color("white").rgb, text=""):
        # color_edited = self.edit_color(color)
        # print(f"Tile ({col},{line}), color ('{color}'), text ('{text}')")
        color_edited = color
        pg.draw.rect(self.gameDisplay,
                     color_edited,
                     [self.square_size_x * col,
                      self.square_size_y * line,
                      self.square_size_x,
                      self.square_size_y])
        if text:
            text_rendered = self.font.render(text, True, self.color_font)
            self.gameDisplay.blit(text_rendered, dest=(self.square_size_x * col + 1,
                                                       self.square_size_y * line))
        # draw border
        if self.show_border:
            pg.draw.rect(self.gameDisplay,
                         self.edit_color(Color("black")),
                         [self.square_size_x * col,
                          self.square_size_y * line,
                          self.square_size_x,
                          self.square_size_y],
                         TILE_BORDER_SIZE)

    def display(self):
        self.for_each_cell(self.draw_cell)
        pg.display.update()
        time.sleep(DISPLAY_TIME)

    def edit_color(self, color):
        return tuple(int(c * 255) for c in color.rgb)
