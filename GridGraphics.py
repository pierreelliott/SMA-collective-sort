import pygame as pg
from random import randint, random
# from CellObjectType import CellObjectType
from colour import Color
import time


WINDOW_SIZE_X = 500
WINDOW_SIZE_Y = 500

# TILE_BORDER_SIZE = 0
TILE_BORDER_SIZE = 1

COLORS = (Color("green"), Color("red"), Color("lightgreen"), Color("salmon"), Color("purple"), Color("blue"),
          Color("brown"), Color("orange"))
FONT_COLOR = Color("black")
FONT_SIZE = 12
AGENT_COLOR = Color("gold")

# DISPLAY_TIME = 0
DISPLAY_TIME = 0.01
# DISPLAY_TIME = 0.1
# DISPLAY_TIME = 0.5
# DISPLAY_TIME = 1


class GridPG:
    def __init__(self, lines, columns, objects, show_border=False, show_agent=True):
        self.show_agent = show_agent
        self.show_border = show_border
        self.square_size_x = WINDOW_SIZE_X  # columns
        self.square_size_y = WINDOW_SIZE_Y  # lines
        print(self.square_size_x, self.square_size_y)
        pg.init()
        pg.font.init()

        self.objects_color = dict()
        i = 0
        for obj_type, _ in objects:
            self.objects_color[obj_type] = self.edit_color(COLORS[i])
            i += 1

        self.color_agent = self.edit_color(AGENT_COLOR)
        self.color_font = self.edit_color(FONT_COLOR)

        self.font = pg.font.Font(
            pg.font.get_default_font(), FONT_SIZE)
        self.gameDisplay = pg.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
        pg.display.set_caption("SMA - Collective Sort")
        pg.display.update()

    def draw_cell(self, col, line, cell, agent):
        # color = Color(rgb=(random(), random(), random()))
        color = self.edit_color(Color("white"))
        object_cell = None
        text = ""

        if cell is not None:
            # There is an object to draw
            color = self.objects_color[cell]
        # else:
        #     print("Problème !")
        if agent is not None:
            # Draw agent
            color = self.color_agent
            text = str(agent.id)

        # if cell.agent and self.show_agent:
        #     if not cell.agent.held:
        #         color = self.color_agent
        #     elif cell.agent.held.type_object == CellObjectType.A:
        #         color = self.color_agent_a
        #     elif cell.agent.held.type_object == CellObjectType.B:
        #         color = self.color_agent_b
        #     else:
        #         print("wtf")
        #     text = cell.agent.name
        # elif cell.obj:
        #     cell_type = cell.type_object()
        #     if cell_type == CellObjectType.A:
        #         color = self.color_a
        #     elif cell_type == CellObjectType.B:
        #         color = self.color_b
        #     else:
        #         print("WTF")
        self.draw_tile(col, line, color=color, text=text)

    def draw_tile(self, col, line, color=Color("white").rgb, text=""):
        # color_edited = self.edit_color(color)
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
        # for cell_i in range(self.cell_number):
        #     self.draw_cell(self.get_cell(cell_i))
        pg.display.update()
        time.sleep(DISPLAY_TIME)

    def edit_color(self, color):
        return tuple(int(c * 255) for c in color.rgb)
