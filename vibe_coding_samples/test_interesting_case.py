import debugpy
from knight_bishop_solver import KnightBishopSolver, Position

# Test case 47 from test_knight_bishop_solver.py
TEST_CASE = {"start": (0, 10), "end": (9, 4), "board_size": (10, 21), "bishop_pos": (4, 6), "expected_moves": 5}


def test_interesting_case():
    """Test case 47 that fails with bidirectional_bfs but should succeed."""
    # Create solver
    solver = KnightBishopSolver(TEST_CASE["board_size"][0], TEST_CASE["board_size"][1], Position(*TEST_CASE["bishop_pos"]))

    # Run test with different methods
    for method in ["bfs", "bidirectional_bfs", "a_star", "ida_star"]:
        result = solver.solve(TEST_CASE["start"], TEST_CASE["end"], method)[0]

        print(f"\nMethod: {method}")
        print(f"Result: {result}")
        print(f"Expected: {TEST_CASE['expected_moves']}")

        if method == "bfs":  # Only BFS should succeed
            assert result == TEST_CASE["expected_moves"], f"BFS should find {TEST_CASE['expected_moves']} moves, but found {result}"


if __name__ == "__main__":
    # Configure debugpy for remote debugging
    debugpy.listen(5678)
    print("Waiting for debugger to connect...")
    debugpy.wait_for_client()

    # Run the test
    test_interesting_case()
