#!/usr/bin/python

# Solve Sudoku puzzle (iterative solution // stack-based).

def is_valid(board, row, col, num):
    # Check if the number is not present in the current row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check if the number is not present in the current 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def find_empty_location(board):
    # Find an empty position (cell with 0)
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None, None  # If the board is filled

def solve_sudoku(board):
    stack = []
    stack.append(board)

    while stack:
        current_board = stack.pop()
        row, col = find_empty_location(current_board)

        if row is None and col is None:
            return current_board

        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = [row[:] for row in current_board]
                new_board[row][col] = num
                stack.append(new_board)

    return None

# Example usage:
# Define the Sudoku puzzle as a 9x9 list with 0 representing empty cells
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solution = solve_sudoku(sudoku_board)

if solution:
    for row in solution:
        print(row)
else:
    print("No solution exists.")
