# For vibe coding discussion:
# https://claude.ai/public/artifacts/aa1ba629-fd33-47aa-b1cf-43ecb97a3280

# To solve a knights and bishops problem: A Knight needs to move from a start to an end position
# without hitting the bishop line of sight on an arbitrary chessboard, not necessarily square.

import heapq
import logging
import time
from collections import deque
from typing import NamedTuple, Set, Tuple

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", force=True
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Position(NamedTuple):
    """A position on the chess board represented as (row, column)."""

    row: int
    col: int


class KnightBishopSolver:
    """
    Solver for finding the minimum number of knight moves required to go from a start position
    to an end position on a chessboard, while avoiding squares that are in a bishop's line of sight.
    """

    def __init__(self, rows: int, cols: int, bishop_pos: Position):
        """
        Initialize the solver with board dimensions and bishop position.

        Note: Start and end positions for the knight are NOT part of the solver's initialization.
        They are passed as parameters to the solve methods.

        Args:
            rows: Number of rows on the board (can be any reasonable size)
            cols: Number of columns on the board (doesn't need to equal rows)
            bishop_pos: Position of the bishop as (row, col)
        """
        self.rows = rows
        self.cols = cols
        self.bishop_pos = bishop_pos

        # Pre-compute bishop's line of sight for efficient lookup
        self.bishop_line_of_sight = self._get_bishop_line_of_sight()

        # Knight's possible moves
        self.knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    def __str__(self) -> str:
        """Return a string representation of the solver."""
        return f"KnightBishopSolver(board_size=({self.rows}, {self.cols}), bishop_pos={self.bishop_pos})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the solver."""
        return f"KnightBishopSolver(rows={self.rows}, cols={self.cols}, bishop_pos=Position(row={self.bishop_pos.row}, col={self.bishop_pos.col}))"

    def _get_bishop_line_of_sight(self) -> Set[Position]:
        """
        Pre-compute all squares that the bishop can see (line of sight).

        Returns:
            A set of Position coordinates that are in the bishop's line of sight.
        """
        logger.info(f"Calculating bishop's line of sight from position {self.bishop_pos}")
        line_of_sight = set()
        b_row, b_col = self.bishop_pos

        # Add bishop's position
        line_of_sight.add(Position(b_row, b_col))
        logger.info(f"Added bishop's position to line of sight: {Position(b_row, b_col)}")

        # Check all four diagonal directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d_row, d_col in directions:
            logger.info(f"Checking direction: ({d_row}, {d_col})")
            r, c = b_row, b_col

            while True:
                r += d_row
                c += d_col

                # Stop if we're off the board
                if not (0 <= r < self.rows and 0 <= c < self.cols):
                    logger.info(f"Position ({r}, {c}) is off the board, stopping this direction")
                    break

                pos = Position(r, c)
                line_of_sight.add(pos)
                logger.info(f"Added position to line of sight: {pos}")

        logger.info(f"Bishop's line of sight contains {len(line_of_sight)} positions: {sorted(line_of_sight)}")
        return line_of_sight

    def _is_valid_position(self, pos: Position) -> bool:
        """
        Check if a position is valid (on the board and not in bishop's line of sight).

        Args:
            pos: Position to check

        Returns:
            True if the position is valid, False otherwise
        """
        # Check if position is on the board
        if not (0 <= pos.row < self.rows and 0 <= pos.col < self.cols):
            return False

        # Check if position is in bishop's line of sight
        if pos in self.bishop_line_of_sight:
            return False

        return True

    def _manhattan_distance(self, pos1: Position, pos2: Position) -> int:
        """
        Calculate Manhattan distance between two positions.

        Args:
            pos1: First position
            pos2: Second position

        Returns:
            Manhattan distance between the positions
        """
        return abs(pos1.row - pos2.row) + abs(pos1.col - pos2.col)

    def _knight_distance_heuristic(self, pos: Position, target: Position) -> int:
        """
        A heuristic for estimating the number of knight moves needed from pos to target.

        This is a lower bound on the actual number of moves required, which is
        important for A* search to find the optimal solution. If we overestimated,
        A* might not find the shortest path.

        Based on the fact that a knight needs at least max(⌈dr/2⌉, ⌈dc/2⌉) moves to cover distance (dr, dc)
        on an empty board.

        Args:
            pos: Current position
            target: Target position

        Returns:
            Estimated minimum number of knight moves required
        """
        dr = abs(pos.row - target.row)
        dc = abs(pos.col - target.col)

        # Special cases for small distances
        if dr == 0 and dc == 0:
            return 0
        if dr == 0 and dc == 1:
            return 3  # Knight needs 3 moves to move just 1 square horizontally
        if dr == 1 and dc == 0:
            return 3  # Knight needs 3 moves to move just 1 square vertically
        if dr == 1 and dc == 1:
            return 2  # Knight needs 2 moves to move diagonally by 1,1

        # General case - divide by 2 and round up
        return max((dr + 1) // 2, (dc + 1) // 2)

    def bfs(self, start: Position, end: Position) -> int:
        """
        Find the minimum number of knight moves from start to end using BFS.

        Args:
            start: Starting position
            end: Target position

        Returns:
            Minimum number of moves required, or -1 if impossible
        """
        # If start equals end, no moves needed
        if start == end:
            return 0

        # Initialize BFS
        queue = deque([(start, 0)])  # (position, moves)
        visited = {start}  # Set of visited positions

        while queue:
            pos, moves = queue.popleft()

            # Check all possible knight moves
            for d_row, d_col in self.knight_moves:
                next_pos = Position(pos.row + d_row, pos.col + d_col)

                # If we've reached the end, return the number of moves
                if next_pos == end:
                    return moves + 1

                # If the position is valid and not visited, add it to the queue
                if self._is_valid_position(next_pos) and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, moves + 1))

        # If we've explored all reachable positions and haven't found the end, it's impossible
        return -1

    def bidirectional_bfs(self, start: Position, end: Position) -> int:
        """
        Find the minimum number of knight moves from start to end using bidirectional BFS.

        Args:
            start: Starting position
            end: Target position

        Returns:
            Minimum number of moves required, or -1 if impossible
        """
        # If start equals end, no moves needed
        if start == end:
            logger.info("Start position equals end position, no moves needed")
            return 0

        logger.info(f"Starting bidirectional BFS from {start} to {end}")
        start_time = time.time()

        # Initialize forward and backward BFS
        forward_queue = deque([(start, 0)])  # (position, moves)
        backward_queue = deque([(end, 0)])  # (position, moves)
        forward_visited = {start: 0}  # position -> moves
        backward_visited = {end: 0}  # position -> moves

        iteration = 0
        last_stats_time = time.time()

        while forward_queue and backward_queue:
            iteration += 1

            # Log statistics every second
            current_time = time.time()
            if current_time - last_stats_time >= 1.0:
                logger.info(
                    f"Iteration {iteration}: Forward queue size: {len(forward_queue)}, "
                    f"Backward queue size: {len(backward_queue)}, "
                    f"Forward visited: {len(forward_visited)}, "
                    f"Backward visited: {len(backward_visited)}"
                )
                last_stats_time = current_time

            # Forward BFS step
            pos, moves = forward_queue.popleft()

            # Skip if we've already processed this position with a better path
            if pos in forward_visited and forward_visited[pos] < moves:
                continue

            for d_row, d_col in self.knight_moves:
                next_pos = Position(pos.row + d_row, pos.col + d_col)
                if self._is_valid_position(next_pos):
                    # Only add if we haven't seen this position or found a better path
                    if next_pos not in forward_visited or moves + 1 < forward_visited[next_pos]:
                        forward_visited[next_pos] = moves + 1
                        forward_queue.append((next_pos, moves + 1))
                        if next_pos in backward_visited:
                            total_moves = moves + 1 + backward_visited[next_pos]
                            elapsed_time = time.time() - start_time
                            logger.info(
                                f"Path found after {iteration} iterations: {total_moves} moves "
                                f"(forward: {moves + 1}, backward: {backward_visited[next_pos]})"
                            )
                            logger.info(f"Search completed in {elapsed_time:.2f} seconds")
                            return total_moves

            # Backward BFS step
            pos, moves = backward_queue.popleft()

            # Skip if we've already processed this position with a better path
            if pos in backward_visited and backward_visited[pos] < moves:
                continue

            for d_row, d_col in self.knight_moves:
                next_pos = Position(pos.row + d_row, pos.col + d_col)
                if self._is_valid_position(next_pos):
                    # Only add if we haven't seen this position or found a better path
                    if next_pos not in backward_visited or moves + 1 < backward_visited[next_pos]:
                        backward_visited[next_pos] = moves + 1
                        backward_queue.append((next_pos, moves + 1))
                        if next_pos in forward_visited:
                            total_moves = moves + 1 + forward_visited[next_pos]
                            elapsed_time = time.time() - start_time
                            logger.info(
                                f"Path found after {iteration} iterations: {total_moves} moves "
                                f"(forward: {forward_visited[next_pos]}, backward: {moves + 1})"
                            )
                            logger.info(f"Search completed in {elapsed_time:.2f} seconds")
                            return total_moves

        elapsed_time = time.time() - start_time
        logger.warning(f"No path found after {iteration} iterations and {elapsed_time:.2f} seconds")
        return -1

    def a_star(self, start: Position, end: Position) -> int:
        """
        Find the minimum number of knight moves from start to end using A* search algorithm.

        Args:
            start: Starting position
            end: Target position

        Returns:
            Minimum number of moves required, or -1 if impossible
        """
        # If start equals end, no moves needed
        if start == end:
            return 0

        # Initialize A* search
        # Priority queue with (f_score, moves, position)
        # f_score = g_score (moves so far) + h_score (heuristic estimate to goal)
        open_set = [(self._knight_distance_heuristic(start, end), 0, start)]
        # Dictionary to track g_scores
        g_scores = {start: 0}
        # Set to track visited nodes
        closed_set = set()

        while open_set:
            _, moves, pos = heapq.heappop(open_set)

            # Skip if we've already processed this position with a better path
            if pos in closed_set and g_scores[pos] < moves:
                continue

            # Mark as processed
            closed_set.add(pos)

            # Check all possible knight moves
            for d_row, d_col in self.knight_moves:
                next_pos = Position(pos.row + d_row, pos.col + d_col)

                # If we've reached the end, return the number of moves
                if next_pos == end:
                    return moves + 1

                # If the position is valid
                if self._is_valid_position(next_pos):
                    next_g_score = moves + 1

                    # If we haven't seen this node before, or we found a better path
                    if next_pos not in g_scores or next_g_score < g_scores[next_pos]:
                        g_scores[next_pos] = next_g_score
                        f_score = next_g_score + self._knight_distance_heuristic(next_pos, end)
                        heapq.heappush(open_set, (f_score, next_g_score, next_pos))

        # If we've explored all reachable positions and haven't found the end, it's impossible
        return -1

    def ida_star(self, start: Position, end: Position) -> int:
        """
        Find the minimum number of knight moves from start to end using IDA* algorithm.
        IDA* is a memory-efficient version of A* that uses depth-first search with iterative deepening.

        Args:
            start: Starting position
            end: Target position

        Returns:
            Minimum number of moves required, or -1 if impossible
        """
        # If start equals end, no moves needed
        if start == end:
            return 0

        # Initial bound is the heuristic estimate from start to end
        bound = self._knight_distance_heuristic(start, end)

        # Path of positions we've taken so far
        path = []

        def search(pos, g, bound):
            """Recursive depth-first search with bound."""
            f = g + self._knight_distance_heuristic(pos, end)

            # If f exceeds bound, return f as the new bound
            if f > bound:
                return f

            # If we've reached the end, return -g (negative to indicate success)
            if pos == end:
                return -g

            min_bound = float("inf")

            # Check all possible knight moves
            for d_row, d_col in self.knight_moves:
                next_pos = Position(pos.row + d_row, pos.col + d_col)

                # If the position is valid and not already in our path
                if self._is_valid_position(next_pos) and next_pos not in path:
                    path.append(next_pos)
                    t = search(next_pos, g + 1, bound)

                    # If t is negative, we found the end
                    if t < 0:
                        return t

                    # Update min_bound
                    if t < min_bound:
                        min_bound = t

                    path.pop()

            return min_bound

        # Iteratively deepen the bound until we find a solution
        while True:
            path = [start]
            t = search(start, 0, bound)

            # If t is negative, we found the end, so convert back to positive
            if t < 0:
                return -t

            # If t is infinity, we've explored all possible paths and found no solution
            if t == float("inf"):
                return -1

            # Otherwise, update the bound and try again
            bound = t

    def solve(self, start: Tuple[int, int], end: Tuple[int, int], method: str = "auto") -> Tuple[int, float]:
        """
        Solve the knight's path problem using the specified method.

        Args:
            start: Starting position as (row, col)
            end: Target position as (row, col)
            method: Solving method to use ("bfs", "bidirectional_bfs", "a_star", "ida_star", or "auto")

        Returns:
            Tuple of (minimum number of moves required, time taken in seconds)
        """
        # Convert tuple positions to Position objects
        start_pos = Position(*start)
        end_pos = Position(*end)

        logger.info(f"Solving knight path from {start_pos} to {end_pos} using method: {method}")

        # Auto-select method based on board size
        if method == "auto":
            if self.rows <= 8 and self.cols <= 8:
                method = "bidirectional_bfs"
                logger.info("Auto-selected bidirectional_bfs for small board (≤8x8)")
            else:
                method = "a_star"
                logger.info("Auto-selected a_star for larger board (>8x8)")

        # Record start time
        start_time = time.time()

        # Solve using selected method
        if method == "bfs":
            result = self.bfs(start_pos, end_pos)
        elif method == "bidirectional_bfs":
            result = self.bidirectional_bfs(start_pos, end_pos)
        elif method == "a_star":
            result = self.a_star(start_pos, end_pos)
        elif method == "ida_star":
            result = self.ida_star(start_pos, end_pos)
        else:
            raise ValueError(f"Unknown method: {method}")

        # Calculate time taken
        time_taken = time.time() - start_time

        # Log result
        if result == -1:
            logger.warning(f"No path found using {method} in {time_taken:.2f} seconds")
        else:
            logger.info(f"Found path with {result} moves using {method} in {time_taken:.2f} seconds")

        return result, time_taken


# Example usage
def main():
    # Example 1: Standard 8x8 chessboard
    rows, cols = 8, 8
    start = (0, 0)  # Bottom left corner
    end = (7, 7)  # Top right corner
    bishop_pos = (3, 3)  # Center bishop

    # Create solver
    solver = KnightBishopSolver(rows, cols, bishop_pos)

    # Solve using different methods and measure performance
    methods = ["bfs", "bidirectional_bfs", "a_star", "ida_star", "auto"]

    print(f"Example 1 - Board Size: {rows}x{cols}")
    print(f"Start: {start}, End: {end}, Bishop: {bishop_pos}")
    print("-" * 60)

    for method in methods:
        moves, time_taken = solver.solve(start, end, method)

        if moves == -1:
            result = "impossible"
        else:
            result = f"{moves} moves"

        print(f"Method: {method.ljust(16)} Result: {result.ljust(12)} Time: {time_taken:.6f} seconds")

    # Example 2: Non-square board
    print("\n\nExample 2 - Non-square board")
    rows, cols = 10, 6
    start = (2, 3)
    end = (8, 2)
    bishop_pos = (5, 1)

    # Create a new solver for the non-square board
    solver = KnightBishopSolver(rows, cols, bishop_pos)

    print(f"Board Size: {rows}x{cols}")
    print(f"Start: {start}, End: {end}, Bishop: {bishop_pos}")
    print("-" * 60)

    # Use only the auto method for this example
    moves, time_taken = solver.solve(start, end, "auto")

    if moves == -1:
        result = "impossible"
    else:
        result = f"{moves} moves"

    print(f"Method: auto            Result: {result.ljust(12)} Time: {time_taken:.6f} seconds")


if __name__ == "__main__":
    main()
