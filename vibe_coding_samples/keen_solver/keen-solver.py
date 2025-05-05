from math import prod

import numpy as np


def solve_keen(puzzle_size, cages):
    """
    Solve a Keen puzzle.

    Args:
        puzzle_size: Size of the puzzle (e.g., 6 for a 6x6 grid)
        cages: List of tuples (target, operation, cells) where:
               - target is the target value
               - operation is '+', '-', '*', '/', or None (for single-cell cages)
               - cells is a list of (row, col) tuples for cells in this cage

    Returns:
        A numpy array representing the solution, or None if no solution exists
    """
    # Create empty grid
    grid = np.zeros((puzzle_size, puzzle_size), dtype=int)

    def is_valid(grid, row, col, num):
        """Check if placing num at (row, col) violates row/column constraints"""
        # Check row
        if num in grid[row, :]:
            return False

        # Check column
        if num in grid[:, col]:
            return False

        return True

    def get_possible_values(target, op, size):
        """Get possible values for a cage based on its operation and target"""
        if op == "*":
            # For multiplication, find all possible factor combinations
            def factorize(n, size, start=1):
                if size == 1:
                    return [[n]] if 1 <= n <= puzzle_size else []
                result = []
                for i in range(start, puzzle_size + 1):
                    if n % i == 0:
                        for factors in factorize(n // i, size - 1, i):
                            result.append([i] + factors)
                return result

            return factorize(target, size)
        elif op == "+":
            # For addition, find all combinations that sum to target
            def find_sums(n, size, start=1):
                if size == 1:
                    return [[n]] if 1 <= n <= puzzle_size else []
                result = []
                for i in range(start, min(n - size + 1, puzzle_size + 1)):
                    for sums in find_sums(n - i, size - 1, i):
                        result.append([i] + sums)
                return result

            return find_sums(target, size)
        elif op == "-":
            # For subtraction, only valid for 2 cells
            if size != 2:
                return []
            return [[a, b] for a in range(1, puzzle_size + 1) for b in range(1, puzzle_size + 1) if abs(a - b) == target]
        elif op == "/":
            # For division, only valid for 2 cells
            if size != 2:
                return []
            return [[a, b] for a in range(1, puzzle_size + 1) for b in range(1, puzzle_size + 1) if max(a, b) / min(a, b) == target]
        return []

    def satisfies_cages(grid, cages):
        """Check if the current (partial) grid satisfies all cage constraints"""
        for target, op, cells in cages:
            # Skip checking if any cell in the cage is still empty
            if any(grid[r, c] == 0 for r, c in cells):
                continue

            values = [grid[r, c] for r, c in cells]

            if op == "+":
                if sum(values) != target:
                    return False
            elif op == "-":
                if len(values) == 2 and abs(values[0] - values[1]) != target:
                    return False
            elif op == "*":
                if prod(values) != target:
                    return False
            elif op == "/":
                if len(values) == 2 and max(values) / min(values) != target:
                    return False
            elif op is None:
                if values[0] != target:
                    return False

        return True

    def solve_partial_cages(grid, cages):
        """Try to fill cells in cages that have limited possibilities"""
        changes = False

        for target, op, cells in cages:
            # Skip if any cell in the cage is already filled
            if any(grid[r, c] != 0 for r, c in cells):
                continue

            # Get possible values for this cage
            possible_values = get_possible_values(target, op, len(cells))

            # Filter out values that conflict with existing numbers in rows/columns
            valid_values = []
            for values in possible_values:
                valid = True
                for (r, c), val in zip(cells, values):
                    if not is_valid(grid, r, c, val):
                        valid = False
                        break
                if valid:
                    valid_values.append(values)

            # If there's only one possibility, fill the cage
            if len(valid_values) == 1:
                for (r, c), val in zip(cells, valid_values[0]):
                    grid[r, c] = val
                    changes = True

        return changes, grid

    def backtrack(grid, row=0, col=0):
        """Solve the puzzle using backtracking"""
        if row == puzzle_size:
            return True

        next_row = row + (col + 1) // puzzle_size
        next_col = (col + 1) % puzzle_size

        if grid[row, col] != 0:
            return backtrack(grid, next_row, next_col)

        for num in range(1, puzzle_size + 1):
            if is_valid(grid, row, col, num):
                grid[row, col] = num
                if satisfies_cages(grid, cages):
                    if backtrack(grid, next_row, next_col):
                        return True
                grid[row, col] = 0

        return False

    # Try to solve partial cages before backtracking
    has_changes = True
    while has_changes:
        has_changes, grid = solve_partial_cages(grid, cages)

    if backtrack(grid):
        return grid
    else:
        return None


def print_puzzle(grid, cages):
    """Print the puzzle solution with ASCII art"""
    size = len(grid)

    # Create a grid of cell borders
    borders = [[" " for _ in range(size * 2 + 1)] for _ in range(size * 2 + 1)]

    # Fill in the corners
    for i in range(0, size * 2 + 1, 2):
        for j in range(0, size * 2 + 1, 2):
            borders[i][j] = "+"

    # Fill in the numbers
    for i in range(size):
        for j in range(size):
            borders[i * 2 + 1][j * 2 + 1] = str(grid[i][j])

    # Draw cage borders
    for _, _, cells in cages:
        for r, c in cells:
            # Convert to border coordinates
            br = r * 2 + 1
            bc = c * 2 + 1

            # Check adjacent cells in the same cage
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in cells:
                    # If adjacent cell is in same cage, remove border
                    if dr == 0:  # horizontal
                        borders[br][bc + dc] = " "
                    else:  # vertical
                        borders[br + dr][bc] = " "
                else:
                    # If adjacent cell is not in same cage, add border
                    if dr == 0:  # horizontal
                        borders[br][bc + dc] = "|"
                    else:  # vertical
                        borders[br + dr][bc] = "-"

    # Print the puzzle
    for row in borders:
        print("".join(row))


# Example usage
puzzle_size = 6
cages = [
    (11, "+", [(0, 0), (0, 1), (1, 0)]),
    (12, "*", [(0, 2), (1, 1), (1, 2)]),
    (2, "-", [(0, 3), (0, 4)]),
    (2, "/", [(0, 5), (1, 5)]),
    (2, "/", [(1, 3), (2, 3)]),
    (8, "*", [(1, 4), (2, 4), (3, 4)]),
    (8, "+", [(2, 0), (3, 0), (3, 1)]),
    (540, "*", [(2, 1), (2, 2), (3, 2), (3, 3)]),
    (4, "-", [(2, 5), (3, 5)]),
    (6, "*", [(4, 0), (5, 0)]),
    (2, "-", [(4, 1), (5, 1)]),
    (9, "+", [(4, 2), (4, 3)]),
    (2, "/", [(4, 4), (5, 4)]),
    (6, "+", [(4, 5), (5, 5)]),
    (1, "-", [(5, 2), (5, 3)]),
]


def validate_cages(puzzle_size, cages):
    """Check that every cell is in exactly one cage."""
    cell_count = {}
    for idx, (_, _, cells) in enumerate(cages):
        for r, c in cells:
            if (r, c) in cell_count:
                raise ValueError(f"Cell ({r},{c}) is in multiple cages! Cage indices: {cell_count[(r,c)]} and {idx}")
            if not (0 <= r < puzzle_size and 0 <= c < puzzle_size):
                raise ValueError(f"Cell ({r},{c}) is outside the grid!")
            cell_count[(r, c)] = idx
    # Check for missing cells
    for r in range(puzzle_size):
        for c in range(puzzle_size):
            if (r, c) not in cell_count:
                raise ValueError(f"Cell ({r},{c}) is not in any cage!")
    print("Validation successful: every cell is in exactly one cage.")


validate_cages(puzzle_size, cages)

solution = solve_keen(puzzle_size, cages)

if solution is not None:
    print("Solution found:")
    print_puzzle(solution, cages)
else:
    print("No solution found. The puzzle might be incorrectly specified.")
