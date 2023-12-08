import random


class SudokuGenerator:

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for i in range(row_length)]
                      for j in range(row_length)]
        self.box_length = 3

    # 2D board method
    def get_board(self):
        return self.board

    # underlying board method
    def print_board(self):
        for i in range(self.row_length):
            print(self.board[i])

    # method to check validity in row
    def valid_in_row(self, row, num):
        row_list = [i for i in self.board[row]]
        if num in row_list:
            return False
        return True

    # method to check validity in column
    def valid_in_col(self, col, num):
        col_list = [self.board[i][col] for i in range(9)]
        if num in col_list:
            return False
        return True

    # method to check if 3x3 box is valid
    def valid_in_box(self, row_start, col_start, num):
        box_list = []
        for i in range(3):
            box_list.append(self.board[row_start + i][col_start])
        for i in range(3):
            box_list.append(self.board[row_start + i][col_start + 1])
        for i in range(3):
            box_list.append(self.board[row_start + i][col_start + 2])
        if num in box_list:
            return False
        return True

    # method to check if user can edit cell
    def is_valid(self, row, col, num):
        indices = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        for i in range(3):
            if row in indices[i]:
                new_row = i * 3
            if col in indices[i]:
                new_col = i * 3
        if self.valid_in_row(row, num):
            if self.valid_in_col(col, num):
                if self.valid_in_box(new_row, new_col, num):
                    return True
        return False

    # method that fills 3x3 box with integers
    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1))
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                self.board[row][col] = random.choice(nums)
                nums.remove(self.board[row][col])

    # method to fill diagonal boxes
    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

    Parameters:
    row, col specify the coordinates of the first empty (0) cell

    Return:
    boolean (whether or not we could solve the board)
    '''

    # method that fills the remaining boxes
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
      DO NOT CHANGE
      Provided for students
      Constructs a solution by calling fill_diagonal and fill_remaining

      Parameters: None
      Return: None
      '''

    # Fills remaining cells in
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

        '''
        Removes the appropriate number of cells from the board
        This is done by setting some values to 0
        Should be called after the entire solution has been constructed
        i.e. after fill_values has been called

        NOTE: Be careful not to 'remove' the same cell multiple times
        i.e. if a cell is already 0, it cannot be removed again

    	Parameters: None
    	Return: None
        '''

    # takes the difficulty and removes the according amount of cells
    def remove_cells(self):
        removed = []
        while True:
            if len(removed) == self.removed_cells:
                break
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            cells = [row, col]
            if cells not in removed:
                removed.append(cells)
                continue
        for i in range(self.removed_cells):
            self.board[removed[i][0]][removed[i][1]] = 0


# function to generate the sudoku board
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board
