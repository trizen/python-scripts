#!/usr/bin/python

# Author: Trizen
# Date: 12 February 2024
# https://github.com/trizen

# Solve Sudoku puzzle (iterative solution), if it has a unique solution.

def find_empty_locations(board):
    empty_locations = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_locations.append((i, j))
    return empty_locations

def solve_sudoku(board):

    prev_len = 0

    while True:

        empty_locations = find_empty_locations(board)

        if len(empty_locations) == 0:
            break   # it's solved

        if len(empty_locations) == prev_len:
            return None     # stuck

        for i, j in empty_locations:

            possible_values = set(range(1, 10))
            for x in range(9):
                possible_values.discard(board[i][x])  # check row
                possible_values.discard(board[x][j])  # check column
                if len(possible_values) == 1: break

            if len(possible_values) == 1:
                board[i][j] = possible_values.pop()
                continue

            # Check 3x3 box
            box_row = (i // 3) * 3
            box_col = (j // 3) * 3
            for x in range(3):
                for y in range(3):
                    possible_values.discard(board[box_row + x][box_col + y])
                    if len(possible_values) == 1: break
                if len(possible_values) == 1: break

            if len(possible_values) == 1:
                board[i][j] = possible_values.pop()

        prev_len = len(empty_locations)

    return board

# Example usage:
board = [
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

solved_board = solve_sudoku(board)
if solved_board:
    for row in solved_board:
        print(row)
else:
    print("No unique solution exists.")
