class SudokuSolver:
  #self.board = []
  def __init__(self,board):
    self.board = board
    # self.board = [
    #       [0, 6, 0, 0, 7, 2, 0, 0, 1], 
    #       [8, 0, 0, 1, 3, 6, 5, 0, 0], 
    #       [0, 0, 3, 4, 0, 0, 0, 0, 0], 
    #       [2, 0, 0, 6, 5, 0, 0, 3, 0], 
    #       [0, 0, 6, 0, 0, 7, 0, 1, 0], 
    #       [0, 0, 0, 2, 0, 0, 8, 6, 4], 
    #       [9, 0, 7, 0, 8, 4, 0, 0, 0], 
    #       [0, 0, 8, 0, 0, 9, 0, 7, 0], 
    #       [0, 0, 0, 7, 2, 1, 0, 8, 3]]
    # self.board = [
    #       [3, 0, 6, 5, 0, 8, 4, 0, 0], 
    #       [5, 2, 0, 0, 0, 0, 0, 0, 0], 
    #       [0, 8, 7, 0, 0, 0, 0, 3, 1], 
    #       [0, 0, 3, 0, 1, 0, 0, 8, 0], 
    #       [9, 0, 0, 8, 6, 3, 0, 0, 5], 
    #       [0, 5, 0, 0, 9, 0, 6, 0, 0], 
    #       [1, 3, 0, 0, 0, 0, 2, 5, 0], 
    #       [0, 0, 0, 0, 0, 0, 0, 7, 4], 
    #       [0, 0, 5, 2, 0, 6, 3, 0, 0]]

  def print_board(self):
    for row in range(len(self.board)):
      if row%3==0 and row!=0:
          print("---------------------")
      for col in range(len(self.board[0])):
        if col%3==0 and col!=0:
          print("| ", end="")
        print(str(self.board[row][col]) + " ",end="")
      print()
  
  def is_config_valid(self,row,col,guess):
    
    # Check if the guess value is present in the row
    for j in range(len(self.board[row])):
      if self.board[row][j]==guess:# and j!=col:
        return False
    
    # Check if the guess value is present in the col
    for i in range(len(self.board)):
      if self.board[i][col]==guess:# and i!=row:
        return False
      
    # Calculate the active grid/box 
    grid_row = row//3
    grid_col = col//3

    # Check if the guess value is present in the grid
    for i in range(grid_row*3, grid_row*3 + 3):
      for j in range(grid_col*3, grid_col*3 + 3):
        if self.board[i][j]==guess:# and i!=row and j!=col:
          return False
    
    # Guess value does not violate any conditions yet
    # Hence, this is presently found to be a valid Sudoku configuration
    return True

  def solve_sudoku(self):

    # Step 1: Find an empty cell i.e. cell value = 0
    row, col = self.find_empty_cell()

    # Step 1.1: If empty cell is not found, then puzzle has been solved
    if row is None: return True

    # Step 2: Try placing values 1-9 in an empty cell
    # If a value fits, proceed to place values in remaining empty cells
    for guess in range(1,10):
      if self.is_config_valid(row,col,guess):
        self.board[row][col] = guess
        if self.solve_sudoku():
          return True

      # If value doesn't fit or solution is not found, backtrack and try another value
      self.board[row][col] = 0

    # If no solution is found then return False
    return False

  def find_empty_cell(self):
    # Iterate from left to right, then top to bottom looking for an empty cell
    for row in range(len(self.board)):
      for col in range(len(self.board[0])):
        if self.board[row][col]==0:
          return row,col
    return None,None

# awesome = SudokuSolver([])
# print("Input: ")
# awesome.print_board()
# awesome.solve_sudoku()
# print("______________________")
# print("Solved Sudoku: ")
# awesome.print_board()