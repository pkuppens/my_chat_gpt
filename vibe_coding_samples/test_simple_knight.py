import pytest
from knight_bishop_solver import KnightBishopSolver, Position
from test_knight_bishop_solver import TEST_CASES


@pytest.mark.knight
def test_simple_case():
    """Test the first test case from TEST_CASES."""
    # Use the first test case from TEST_CASES
    start = (13, 29)
    end = (5, 15)
    board_size = (36, 30)
    bishop_pos = (24, 25)
    expected = 8

    # Create solver
    solver = KnightBishopSolver(board_size[0], board_size[1], Position(*bishop_pos))

    # Test with bfs method
    result, time_taken = solver.solve(start, end, "bfs")

    print("\nTest results:")
    print(f"Board size: {board_size}")
    print(f"Start: {start}, End: {end}, Bishop: {bishop_pos}")
    print(f"Result: {result} moves")
    print(f"Expected: {expected} moves")
    print(f"Time: {time_taken:.6f} seconds")

    # We expect the result to match the expected value
    assert result == expected, f"Path not found or incorrect number of moves. Expected: {expected}, Got: {result}"


@pytest.mark.knight
@pytest.mark.parametrize("start,goal,board_size,bishop_pos,_,expected", TEST_CASES)
def test_bfs_on_all(start, goal, board_size, bishop_pos, _, expected):
    """Test BFS on all test cases from TEST_CASES."""
    # Create solver
    solver = KnightBishopSolver(board_size[0], board_size[1], Position(*bishop_pos))

    # Test with bfs method
    result, time_taken = solver.solve(start, goal, "bfs")

    print("\nTest results for case:")
    print(f"Board size: {board_size}")
    print(f"Start: {start}, End: {goal}, Bishop: {bishop_pos}")
    print(f"Result: {result} moves")
    print(f"Expected: {expected} moves")
    print(f"Time: {time_taken:.6f} seconds")

    # We expect the result to match the expected value
    assert result == expected, f"Path not found or incorrect number of moves. Expected: {expected}, Got: {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "knight"])
