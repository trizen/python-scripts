#!/usr/bin/python

# Author: Trizen
# Date: 12 February 2024
# https://github.com/trizen

# Solve Sudoku puzzle (iterative solution), if it has a unique solution.

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

def find_empty_locations(board):

    empty_locations = []

    # Find all empty positions (cells with 0)
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_locations.append((i, j))

    return empty_locations

def find_empty_location(board):
    # Find an empty position (cell with 0)
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None, None  # If the board is filled

def solve_sudoku_fallback(board):
    row, col = find_empty_location(board)

    if row is None and col is None:
        return True  # Puzzle is solved

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            # Try placing the number
            board[row][col] = num

            # Recursively try to solve the rest of the puzzle
            if solve_sudoku_fallback(board):
                return True

            # If placing the current number doesn't lead to a solution, backtrack
            board[row][col] = 0

    return False  # No solution found


def solve_sudoku(board):

    while True:

        empty_locations = find_empty_locations(board)

        if len(empty_locations) == 0:
            break   # it's solved

        found = False

        # Solve easy cases
        for i, j in empty_locations:
            count = 0
            value = 0
            for n in range(1,10):
                if is_valid(board, i, j, n):
                    count += 1
                    value = n
                    if count > 1: break
            if count == 1:
                board[i][j] = value
                found = True

        if found: continue

        # Solve more complex cases
        stats = [[0]*9 for x in [0]*9]
        for i,j in empty_locations:
            arr = []
            for n in range(1, 10):
                if is_valid(board, i, j, n):
                    arr.append(n)
            stats[i][j] = arr

        cols = [[0]*10 for x in [0]*9]
        rows = [[0]*10 for x in [0]*9]

        for i,j in empty_locations:
            for v in stats[i][j]:
                rows[i][v] += 1
                cols[j][v] += 1

        for i,j in empty_locations:
            for v in stats[i][j]:
                if (cols[j][v] == 1 or rows[i][v] == 1):
                    board[i][j] = v
                    found = True

        if found: continue

        # Give up try brute-force
        solve_sudoku_fallback(board)
        return board

    return board

# Example usage:
# Define the Sudoku puzzle as a 9x9 list with 0 representing empty cells
sudoku_board = [
        [2, 0, 0, 0, 7, 0, 0, 0, 3],
        [1, 0, 0, 0, 0, 0, 0, 8, 0],
        [0, 0, 4, 2, 0, 9, 0, 0, 5],
        [9, 4, 0, 0, 0, 0, 6, 0, 8],
        [0, 0, 0, 8, 0, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 0],
        [7, 2, 1, 9, 0, 8, 0, 6, 0],
        [0, 3, 0, 0, 2, 7, 1, 0, 0],
        [4, 0, 0, 0, 0, 3, 0, 0, 0]
]

solution = solve_sudoku(sudoku_board)

if solution:
    for row in solution:
        print(row)
else:
    print("No unique solution exists.")
