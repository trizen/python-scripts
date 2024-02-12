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

    positions = []

    # Find all empty positions (cells with 0)
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                positions.append([i, j])

    return positions

def solve_sudoku(board):

    prev_len = 0

    while True:

        empty_locations = find_empty_locations(board)

        if len(empty_locations) == 0:
            break   # it's solved

        if len(empty_locations) == prev_len:
            return None     # stuck

        for i,j in empty_locations:
            count = 0
            value = 0
            for n in range(1,10):
                if is_valid(board, i, j, n):
                    count += 1
                    value = n
                    if count > 1: break
            if count == 1:
                board[i][j] = value

        prev_len = len(empty_locations)

    return board

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
    print("No unique solution exists.")
