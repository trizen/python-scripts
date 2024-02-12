#!/usr/bin/python

# Benchmark several algorithms for solving Sudoku.

# Results:
#   Iterative algorithm execution time: 0.043829917907714844
#   Iterative #2 algorithm execution time: 0.040073394775390625
#   Stack-based algorithm execution time: 0.15182018280029297
#   Backtracking algorithm execution time: 0.30015063285827637

import time
import copy

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

def find_empty_locations(board):

    empty_locations = []

    # Find all empty positions (cells with 0)
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_locations.append((i, j))

    return empty_locations

def solve_sudoku_iterative(board):

    while True:

        empty_locations = find_empty_locations(board)

        if len(empty_locations) == 0:
            break   # it's solved

        found = False

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

        # Give up
        solve_sudoku_backtracking(board)
        return board

    return board

def solve_sudoku_iterative_2(board):

    prev_len = 0

    while True:

        empty_locations = find_empty_locations(board)

        if len(empty_locations) == 0:
            break   # it's solved

        if len(empty_locations) == prev_len:
            solve_sudoku_backtracking(board)
            return board

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

def solve_sudoku_stack(board):
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

def solve_sudoku_backtracking(board):
    row, col = find_empty_location(board)

    if row is None and col is None:
        return True  # Puzzle is solved

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            # Try placing the number
            board[row][col] = num

            # Recursively try to solve the rest of the puzzle
            if solve_sudoku_backtracking(board):
                return True

            # If placing the current number doesn't lead to a solution, backtrack
            board[row][col] = 0

    return False  # No solution found

# Your test Sudoku puzzles
puzzles = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 7, 0]
    ],
    [
        [0, 0, 0, 0, 6, 2, 8, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 4],
        [2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 7, 5, 0, 0, 3, 0, 0],
        [0, 0, 9, 0, 0, 0, 2, 0, 0],
        [0, 0, 5, 0, 0, 4, 7, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
        [9, 0, 0, 0, 7, 0, 0, 0, 0],
        [0, 0, 2, 3, 8, 0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0, 3, 0, 0, 0],
        [0, 5, 9, 0, 0, 7, 0, 0, 8],
        [2, 0, 0, 4, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 0, 8, 0],
        [0, 0, 7, 2, 0, 0, 3, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 4, 0],
        [3, 0, 0, 0, 0, 0, 1, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0]
    ],
    [
        [5, 3, 0, 0, 2, 4, 7, 0, 0],
        [0, 0, 2, 0, 0, 0, 8, 0, 0],
        [1, 0, 0, 7, 0, 3, 9, 0, 2],
        [0, 0, 8, 0, 7, 2, 0, 4, 9],
        [0, 2, 0, 9, 8, 0, 0, 7, 0],
        [7, 9, 0, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 3, 0, 5, 0, 6],
        [9, 6, 0, 0, 1, 0, 3, 0, 0],
        [0, 5, 0, 6, 9, 0, 0, 1, 0]
    ],
    [
        [0, 0, 9, 0, 0, 0, 0, 0, 0],
        [4, 0, 7, 0, 0, 0, 2, 0, 0],
        [3, 0, 0, 1, 8, 0, 6, 9, 0],
        [0, 5, 3, 0, 9, 0, 1, 0, 2],
        [2, 0, 4, 6, 0, 3, 0, 0, 9],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 3, 6, 7, 0, 5, 8, 2, 0],
        [5, 0, 0, 0, 3, 0, 9, 0, 0],
        [0, 0, 8, 2, 6, 0, 5, 7, 0]
    ],
    [
        [0, 0, 3, 5, 0, 7, 9, 0, 0],
        [0, 2, 1, 0, 0, 0, 0, 0, 7],
        [9, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 2, 6, 0, 0],
        [0, 9, 0, 0, 3, 4, 0, 0, 0],
        [3, 7, 2, 9, 6, 8, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 1, 0, 4],
        [0, 0, 9, 3, 0, 0, 5, 2, 0],
        [0, 6, 0, 0, 0, 1, 0, 0, 3]
    ],
    [
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
    # Add more Sudoku puzzles here
]

start_time = time.time()
for puzzle in puzzles:
    solve_sudoku_iterative(copy.deepcopy(puzzle))
end_time = time.time()
print("Iterative algorithm execution time:", end_time - start_time)

start_time = time.time()
for puzzle in puzzles:
    solve_sudoku_iterative_2(copy.deepcopy(puzzle))
end_time = time.time()
print("Iterative #2 algorithm execution time:", end_time - start_time)

start_time = time.time()
for puzzle in puzzles:
    solve_sudoku_stack(copy.deepcopy(puzzle))
end_time = time.time()
print("Stack-based algorithm execution time:", end_time - start_time)

start_time = time.time()
for puzzle in puzzles:
    solve_sudoku_backtracking(copy.deepcopy(puzzle))
end_time = time.time()
print("Backtracking algorithm execution time:", end_time - start_time)
