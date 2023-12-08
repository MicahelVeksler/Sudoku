import sys
import pygame
from sudoku_generator import *
from constants import *
from board import Board


# Function that produces the start screen
def start_screen():
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((background))
    font = pygame.font.SysFont("Tahoma", 30)
    title_font = pygame.font.SysFont("Tahoma", 40)

    title = title_font.render("Welcome to Sudoku", 1, white)
    difficulty = font.render("Select Game Mode:", 1, white)
    title_rect = title.get_rect(center=(300, 180))
    diff_rect = difficulty.get_rect(center=(300, 320))

    easy = font.render("EASY", 1, white)
    medium = font.render("MEDIUM", 1, white)
    hard = font.render("HARD", 1, white)
    easy_button = pygame.Surface(
        (easy.get_size()[0] + 5, easy.get_size()[1] + 5))
    easy_button.fill(orange)
    easy_button.blit(easy, (5, 5))
    medium_button = pygame.Surface(
        (medium.get_size()[0] + 5, medium.get_size()[1] + 5))
    medium_button.fill(orange)
    medium_button.blit(medium, (5, 5))
    hard_button = pygame.Surface(
        (hard.get_size()[0] + 5, hard.get_size()[1] + 5))
    hard_button.fill(orange)
    hard_button.blit(hard, (5, 5))

    global easy_rect
    global medium_rect
    global hard_rect
    easy_rect = easy_button.get_rect(center=(80, 400))
    medium_rect = medium_button.get_rect(center=(270, 400))
    hard_rect = hard_button.get_rect(center=(490, 400))

    screen.blit(title, title_rect)
    screen.blit(difficulty, diff_rect)
    screen.blit(easy_button, easy_rect)
    screen.blit(medium_button, medium_rect)
    screen.blit(hard_button, hard_rect)


# Function that produces game over screen
def game_over_screen(win):
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill(background)
    text_font = pygame.font.SysFont("Tahoma", 30)
    title_font = pygame.font.SysFont("Tahoma", 40)
    exit = text_font.render('Exit', 1, white)
    restart = text_font.render('Restart', 1, white)
    global restart_rect
    global exit_rect

    # produces the game won screen
    if win == True:
        gameover_surf = title_font.render('GAME WON!', 1, white)
        gameover_rect = gameover_surf.get_rect(center=(270, 200))
        screen.blit(gameover_surf, gameover_rect)
        restart = pygame.Surface((restart.get_size()[0] + 5, restart.get_size()[1] + 5))
        restart.fill(orange)
        restart.blit(restart, (5, 5))
        restart_rect = restart.get_rect(center=(170, 400))
        screen.blit(restart, restart_rect)

        exit_button = pygame.Surface((exit.get_size()[0] + 5, exit.get_size()[1] + 5))
        exit_button.fill(orange)
        exit_button.blit(exit, (5, 5))
        exit_rect = exit_button.get_rect(center=(370, 400))
        screen.blit(exit_button, exit_rect)

    # produces the game lost screen
    elif win == False:
        gameover_surf = title_font.render('GAME OVER :(', 1, white)
        gameover_rect = gameover_surf.get_rect(center=(270, 200))

        screen.blit(gameover_surf, gameover_rect)
        restart_button = pygame.Surface((restart.get_size()[0] + 5, restart.get_size()[1] + 5))
        restart_button.fill(orange)
        restart_button.blit(restart, (5, 5))
        restart_rect = restart_button.get_rect(center=(170, 400))
        screen.blit(restart_button, restart_rect)

        exit_button = pygame.Surface((exit.get_size()[0] + 5, exit.get_size()[1] + 5))
        exit_button.fill(orange)
        exit_button.blit(exit, (5, 5))
        exit_rect = exit_button.get_rect(center=(370, 400))
        screen.blit(exit_button, exit_rect)


def main():
    state = "start"
    sketched_value = 0

    while True:

        mouse_pos = (0, 0)

        # Start menu
        if state == "start":
            start_screen()

            # handles events
            for event in pygame.event.get():

                # allows user to click the events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                # Starts the game and sets the difficulty based on user's choice
                if easy_rect.collidepoint(mouse_pos):
                    board = Board(screen_width, screen_height, "easy")
                    state = "game"
                elif medium_rect.collidepoint(mouse_pos):
                    board = Board(screen_width, screen_height, "medium")
                    state = "game"
                elif hard_rect.collidepoint(mouse_pos):
                    board = Board(screen_width, screen_height, "hard")
                    state = "game"

        # Gameboard screen
        elif state == "game":

            # Draws the sudoku board
            board.draw()

            # handles events
            for event in pygame.event.get():

                # allows user to click the events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    y, x = mouse_pos

                    # allows user to click individual cells
                    if board.click(x, y) != None:
                        if board.selected_cell != None:
                            board.selected_cell.sketched_value = None
                        click_row, click_col = board.click(x, y)
                        board.select(click_row, click_col)

                    # conditions set to be able to click the buttons
                    if board.reset_rect.collidepoint(mouse_pos):
                        board.reset_to_original()
                        pygame.display.update()
                    elif board.restart_rect.collidepoint(mouse_pos):
                        state = "start"
                    elif board.exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

                # allows user to use keyboard
                elif event.type == pygame.KEYDOWN:

                    match event.key:

                        # allows user to move cells using keyboard to the right
                        case pygame.K_RIGHT:
                            if board.selected_cell == None:
                                board.select(0, 0)
                            elif board.colpos == 8:
                                board.select(board.rowpos, board.colpos)
                            else:
                                board.select(board.rowpos, board.colpos + 1)

                        # allows user to move cells using keyboard to the left
                        case pygame.K_LEFT:
                            if board.selected_cell == None:
                                board.select(0, 0)
                            elif board.colpos == 0:
                                pass
                            else:
                                board.select(board.rowpos, board.colpos - 1)

                        # allows user to move cells using keyboard up
                        case pygame.K_UP:
                            if board.selected_cell == None:
                                board.select(0, 0)
                            elif board.rowpos == 0:
                                board.select(board.rowpos, board.colpos)
                            else:
                                board.select(board.rowpos - 1, board.colpos)

                        # allows user to move cells using keyboard down
                        case pygame.K_DOWN:
                            if board.selected_cell == None:
                                board.select(0, 0)
                            elif board.rowpos == 8:
                                board.select(board.rowpos, board.colpos)
                            else:
                                board.select(board.rowpos + 1, board.colpos)

                        # allows user to input the digits for sudoku
                        case pygame.K_1:
                            board.sketch(1)
                            sketched_value = 1
                        case pygame.K_2:
                            board.sketch(2)
                            sketched_value = 2
                        case pygame.K_3:
                            board.sketch(3)
                            sketched_value = 3
                        case pygame.K_4:
                            board.sketch(4)
                            sketched_value = 4
                        case pygame.K_5:
                            board.sketch(5)
                            sketched_value = 5
                        case pygame.K_6:
                            board.sketch(6)
                            sketched_value = 6
                        case pygame.K_7:
                            board.sketch(7)
                            sketched_value = 7
                        case pygame.K_8:
                            board.sketch(8)
                            sketched_value = 8
                        case pygame.K_9:
                            board.sketch(9)
                            sketched_value = 9

                        # enters and removes the values cases
                        case pygame.K_RETURN:
                            if sketched_value > 0:
                                board.place_number(sketched_value)
                                board.update_board()
                                sketched_value = 0
                        case pygame.K_BACKSPACE:
                            board.clear()
                            board.update_board()

            # Ends the game if board is complete
            if board.is_full():
                state = "gameover"

        # Print game over screen
        elif state == "gameover":
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Print game won screen
                if board.check_board():

                    game_over_screen(True)

                    if restart_rect.collidepoint(mouse_pos):
                        state = "start"
                    elif exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

                # Print game lost screen
                elif not board.check_board():

                    game_over_screen(False)

                    if restart_rect.collidepoint(mouse_pos):
                        state = "start"
                    elif exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
