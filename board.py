from cell import Cell
from sudoku_generator import *
from constants import *
import pygame
import copy


class Board:
    # Initialization of class attributes to display the board
    pygame.init()
    pygame.display.set_caption("Sudoku")
    text_font = pygame.font.SysFont("Tahoma", 30)

    reset = text_font.render('Reset', 1, white)
    restart = text_font.render('Restart', 1, white)
    exit = text_font.render('Exit', 1, white)

    reset_button = pygame.Surface(
        (reset.get_size()[0] + 5, reset.get_size()[1] + 5))
    reset_button.fill(orange)
    reset_button.blit(reset, (5, 5))

    restart_button = pygame.Surface(
        (restart.get_size()[0] + 5, restart.get_size()[1] + 5))
    restart_button.fill(orange)
    restart_button.blit(restart, (5, 5))

    exit_button = pygame.Surface(
        (exit.get_size()[0] + 5, exit.get_size()[1] + 5))
    exit_button.fill(orange)
    exit_button.blit(exit, (5, 5))

    reset_rect = reset_button.get_rect(center=(80, 570))
    restart_rect = restart_button.get_rect(center=(270, 570))
    exit_rect = exit_button.get_rect(center=(490, 570))

    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.sketched = False
        self.selected_cell = None
        self.rowpos = None
        self.colpos = None

        # Set the difficulty
        if difficulty == "easy":
            self.difficulty = 30
        elif difficulty == "medium":
            self.difficulty = 40
        elif difficulty == "hard":
            self.difficulty = 50

        # Create the board
        self.board = generate_sudoku(9, self.difficulty)
        self.old_board = copy.deepcopy(self.board)
        self.cells = [[
            Cell(self.board[i][j], i, j, self.screen) for j in range(9)
        ] for i in range(9)]

    def draw(self):
        self.screen.fill(white)

        # horizontal lines
        for i in range(1, 10):
            pygame.draw.line(self.screen, red,
                             (0, i * (screen_width / 9)),
                             (screen_width, i * (screen_width / 9)), 3)

        # vertical lines
        for i in range(1, 9):
            pygame.draw.line(self.screen, red, (i * (540 / 9), 0),
                             (i * (540 / 9), 540), 3)

        for i in range(0, 10, 3):
            pygame.draw.line(self.screen, black, (0, i * (screen_width / 9)),
                             (screen_width, i * (screen_width / 9)), 8)
        # more vertical lines
        for i in range(0, 9, 3):
            pygame.draw.line(self.screen, black, (i * (540 / 9), 0),
                             (i * (540 / 9), 540), 8)

        # cell values and sketched values
        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw(self.screen)

        # function that outlines the cell that the user selects
        if self.selected_cell != None:
            pygame.draw.rect(self.screen, red,
                             (60 * (self.colpos + 1) - 60, 60 *
                              (self.rowpos + 1) - 60, 60, 60), 2)

            self.selected_cell.sketch(self.screen)

        self.screen.blit(self.reset_button, self.reset_rect)
        self.screen.blit(self.restart_button, self.restart_rect)
        self.screen.blit(self.exit_button, self.exit_rect)

    # select cell method
    def select(self, row, col):
        self.selected_cell = self.cells[row][col]
        self.rowpos = row
        self.colpos = col

    # Method that converts click coordinates to the specific column and row of a cell
    def click(self, x, y):
        if 0 <= x <= 540 and 0 <= y <= 540:
            return (x // 60, y // 60)
        else:
            return None

    # Clear cell method
    def clear(self):
        if self.old_board[self.rowpos][self.colpos] == 0:
            self.selected_cell.set_cell_value(0)
            self.selected_cell.set_sketched_value(None)

    # sketch method
    def sketch(self, value):
        if self.old_board[self.rowpos][self.colpos] == 0:
            self.selected_cell.set_sketched_value(value)
            self.selected_cell.inputted_value = True

    # method that adds a number to the sudoku board
    def place_number(self, value):
        if self.old_board[self.rowpos][self.colpos] == 0:
            self.cells[self.rowpos][self.colpos].value = value

    # method that resets board to original board method
    def reset_to_original(self):
        self.selected_cell = None
        self.board.clear()
        self.cells.clear()
        self.board = copy.deepcopy(self.old_board)
        self.cells = [[
            Cell(self.board[i][j], i, j, self.screen) for j in range(9)
        ] for i in range(9)]

    # method that checks if the board is filled
    def is_full(self):
        zero_count = 0

        for row in self.board:
            for col in row:
                if col == 0:
                    zero_count += 1

        if zero_count == 0:
            return True
        else:
            return False

    # method that updates the board with user input values
    def update_board(self):
        for row in range(9):
            for col in range(9):
                self.board[row][col] = self.cells[row][col].value

    # method to find empty cells
    def find_empty(self):
        for row in self.board:
            for col in row:
                if col == 0:
                    return (row, col)

    # check board method
    def check_board(self):

        # checks each row
        for i in range(len(self.board)):
            if 0 in self.board[i]:
                return False
            for num in range(1, 10):
                if self.board[i].count(num) != 1:
                    return False

        # checks each column
        col_count = []
        for col in range(9):
            for i in range(len(self.board)):
                col_count.append(self.board[i][col])
            for num in range(1, 10):
                if col_count.count(num) != 1:
                    return False
            col_count.clear()

        return True
