import logging
import time

import pytest
from knight_bishop_solver import KnightBishopSolver, Position

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s", datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# Test cases with method included
TEST_CASES = [
    # (start, goal, board_size, bishop_pos, method, expected_moves)
    ((13, 29), (5, 15), (36, 30), (24, 25), "auto", 8),
    ((0, 11), (0, 14), (1, 17), (0, 5), "auto", -1),
    ((21, 2), (41, 4), (78, 6), (45, 2), "auto", 10),
    ((0, 0), (0, 4), (20, 20), (0, 1), "auto", 4),
    ((41, 18), (59, 0), (72, 75), (21, 25), "auto", 12),
    ((16, 54), (50, 13), (55, 63), (48, 61), "auto", 25),
    ((12, 9), (35, 9), (37, 36), (8, 25), "auto", 13),
    ((61, 3), (43, 9), (93, 10), (79, 0), "auto", 10),
    ((29, 21), (7, 14), (34, 22), (32, 5), "auto", 11),
    ((83, 27), (2, 16), (100, 32), (89, 19), "auto", 42),
    ((56, 3), (65, 5), (67, 6), (55, 0), "auto", 5),
    ((28, 9), (21, 23), (48, 29), (44, 4), "auto", 7),
    ((25, 23), (49, 20), (91, 60), (87, 43), "auto", 13),
    ((1, 46), (1, 12), (3, 49), (2, 8), "auto", 18),
    ((6, 33), (35, 62), (37, 64), (22, 12), "auto", 20),
    ((54, 3), (5, 57), (68, 93), (46, 10), "auto", 35),
    ((9, 17), (5, 4), (20, 22), (1, 6), "auto", 7),
    ((36, 14), (4, 1), (83, 15), (63, 7), "auto", 17),
    ((40, 3), (40, 15), (44, 17), (42, 11), "auto", 6),
    ((9, 7), (1, 65), (10, 88), (3, 62), "auto", 30),
    ((38, 15), (1, 41), (73, 82), (0, 14), "auto", 21),
    ((53, 13), (41, 1), (76, 17), (13, 8), "auto", 8),
    ((8, 21), (11, 19), (12, 43), (0, 24), "auto", 3),
    ((7, 74), (59, 66), (90, 96), (22, 54), "auto", 26),
    ((35, 1), (33, 3), (38, 5), (7, 4), "auto", 4),
    ((28, 93), (16, 9), (42, 99), (21, 5), "auto", 42),
    ((11, 5), (15, 2), (16, 6), (3, 4), "auto", 3),
    ((50, 29), (4, 39), (55, 42), (40, 12), "auto", 24),
    ((52, 0), (61, 0), (86, 36), (71, 6), "auto", 5),
    ((45, 17), (8, 6), (55, 27), (50, 18), "auto", 20),
    ((5, 44), (10, 41), (14, 53), (9, 52), "auto", 4),
    ((34, 19), (31, 34), (48, 38), (40, 34), "auto", 8),
    ((16, 68), (10, 1), (51, 96), (38, 8), "auto", 35),
    ((38, 31), (55, 10), (83, 74), (11, 65), "auto", 14),
    ((80, 4), (37, 27), (90, 60), (18, 12), "auto", 22),
    ((49, 72), (52, 10), (61, 76), (34, 20), "auto", 31),
    ((1, 64), (35, 49), (60, 65), (0, 35), "auto", 17),
    ((8, 32), (20, 30), (98, 36), (35, 6), "auto", 6),
    ((0, 9), (35, 9), (85, 48), (43, 19), "auto", 19),
    ((22, 10), (6, 6), (88, 63), (58, 29), "auto", 8),
    ((23, 35), (3, 28), (27, 42), (26, 15), "auto", 11),
    ((1, 0), (11, 47), (18, 71), (2, 31), "auto", 25),
    ((28, 62), (31, 44), (76, 90), (46, 9), "auto", 9),
    ((40, 11), (13, 0), (86, 55), (16, 24), "auto", 14),
    ((16, 45), (15, 24), (20, 75), (0, 67), "auto", 12),
    ((53, 22), (9, 38), (56, 49), (45, 41), "auto", 22),
    ((13, 63), (12, 46), (20, 68), (2, 34), "auto", 10),
    ((0, 10), (9, 4), (10, 21), (4, 6), "auto", 5),
    ((35, 0), (5, 1), (37, 4), (36, 2), "auto", 15),
    ((12, 14), (4, 37), (23, 51), (1, 47), "auto", 13),
    ((2, 84), (8, 69), (9, 93), (3, 62), "auto", 9),
]


def _run_test_case(start, goal, board_size, bishop_pos, method, expected):
    """Helper function to run a single test case."""
    logger.info(f"Creating solver for board size {board_size} with bishop at {bishop_pos}")
    solver = KnightBishopSolver(board_size[0], board_size[1], Position(*bishop_pos))

    logger.info(f"Starting solve with method={method} from {start} to {goal}")
    start_time = time.time()
    result = solver.solve(start, goal, method)[0]
    end_time = time.time()
    execution_time = end_time - start_time

    logger.info(
        f"Test completed in {execution_time:.6f}s - "
        f"start={start}, goal={goal}, board={board_size}, bishop={bishop_pos}, "
        f"method={method}, expected={expected}, result={result}"
    )

    assert result == expected, f"Test failed: start={start}, goal={goal}, board={board_size}, bishop={bishop_pos}, method={method}"


@pytest.mark.parametrize("start,goal,board_size,bishop_pos,method,expected", TEST_CASES)
def test_all_cases(start, goal, board_size, bishop_pos, method, expected):
    """Test all cases with their specified methods."""
    logger.info(f"Running test case: board={board_size}, start={start}, goal={goal}, method={method}")
    _run_test_case(start, goal, board_size, bishop_pos, method, expected)


def test_specific_case():
    """Test a specific case with different methods."""
    # Example: Test the first case with all methods, especially for cases like 5 and 9 this matters
    start, goal, board_size, bishop_pos, _, expected = TEST_CASES[5]
    logger.info(f"Running specific test case with multiple methods: board={board_size}, start={start}, goal={goal}")

    for method in ["bidirectional_bfs", "a_star"]:
        logger.info(f"Testing with method: {method}")
        _run_test_case(start, goal, board_size, bishop_pos, method, expected)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
