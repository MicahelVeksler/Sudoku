import pygame
from constants import *


class Cell:
    # Initialize class attributes for showing the cells
    pygame.init()
    board_num_font = pygame.font.SysFont("Tahoma", 30)
    sketch_font = pygame.font.SysFont("Tahoma", 24)

    # cell class constructor
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = None
        self.inputted_value = False

    # method to set cell values
    def set_cell_value(self, value):
        self.value = value

    # sets sketch value
    def set_sketched_value(self, value):
        self.sketched_value = value

    # method to draw the cells value
    def draw(self, screen):

        # Draw sketched value
        if 0 < self.value < 10 and self.inputted_value == True:
            sketch_surf = self.sketch_font.render(str(self.value), 1, grey)
            sketch_rect = sketch_surf.get_rect(
                center=(60 * (self.col + 1) - 38, 60 * (self.row + 1) - 38))
            screen.blit(sketch_surf, sketch_rect)

        # Draw cell value
        elif 0 < self.value < 10:
            cell_surf = self.board_num_font.render(str(self.value), 1, black)
            cell_rect = cell_surf.get_rect(center=(60 * (self.col + 1) - 30,
                                                   60 * (self.row + 1) - 30))
            screen.blit(cell_surf, cell_rect)

    def sketch(self, screen):
        # Draw sketched value
        if self.sketched_value != None:

            sketch_surf = self.sketch_font.render(str(self.sketched_value), 1,
                                                  grey)
            sketch_rect = sketch_surf.get_rect(
                center=(60 * (self.col + 1) - 38, 60 * (self.row + 1) - 38))
            screen.blit(sketch_surf, sketch_rect)
