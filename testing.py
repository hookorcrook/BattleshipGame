import unittest
from board import initialize_board, display_board, update_board
from validator import validate_position, place_ship
from highscores import save_high_score, get_high_score
import os

class TestBattleship(unittest.TestCase):
    def setUp(self):
        """
        Set up for tests. Initialize a board for use in tests.
        """
        self.board = initialize_board()
        self.ships = [
            ("Destroyer", 3),
            ("Cruiser", 5),
            ("Battleship", 7),
            ("Aircraft Carrier", 9)
        ]

    def test_initialize_board(self):
        """
        Test that the board initializes correctly with empty spaces.
        """
        board = initialize_board()
        self.assertEqual(len(board), 26)  # Check row count (A-Z)
        self.assertEqual(len(board[0]), 10)  # Check column count (0-9)
        self.assertTrue(all(cell == ' ' for row in board for cell in row))  # Ensure all cells are empty

    def test_validate_position_valid(self):
        """
        Test valid ship placement positions.
        """
        valid = validate_position(self.board, 3, (10, 5), 'H')  # Destroyer horizontally at K6
        self.assertTrue(valid)

        valid = validate_position(self.board, 5, (5, 3), 'V')  # Cruiser vertically at F4
        self.assertTrue(valid)

    def test_validate_position_invalid(self):
        """
        Test invalid ship placement positions.
        """
        # Out of bounds placement
        invalid = validate_position(self.board, 3, (0, 8), 'H')  # Goes beyond right edge
        self.assertFalse(invalid)

        invalid = validate_position(self.board, 5, (24, 2), 'V')  # Goes beyond bottom edge
        self.assertFalse(invalid)

        # Overlapping ships
        place_ship(self.board, 3, (10, 5), 'H')  # Place a Destroyer horizontally at K6
        invalid = validate_position(self.board, 3, (10, 5), 'V')  # Try to overlap another Destroyer
        self.assertFalse(invalid)

    def test_place_ship(self):
        """
        Test placing ships on the board.
        """
        placed = place_ship(self.board, 3, (10, 5), 'H')  # Destroyer horizontally at K6
        self.assertTrue(placed)

        # Check board updated correctly
        self.assertEqual(self.board[10][4], 'S')
        self.assertEqual(self.board[10][5], 'S')
        self.assertEqual(self.board[10][6], 'S')

    def test_update_board(self):
        """
        Test updating the board for hits and misses.
        """
        update_board(self.board, 5, 5, 'X')  # Mark a hit at F6
        self.assertEqual(self.board[5][5], 'X')

        update_board(self.board, 6, 6, 'O')  # Mark a miss at G7
        self.assertEqual(self.board[6][6], 'O')

    def test_save_and_get_high_score(self):
        """
        Test saving and retrieving high scores.
        """
        file_name = "test_highscores.txt"
        # Remove file if it exists to start clean
        if os.path.exists(file_name):
            os.remove(file_name)

        save_high_score(file_name, "Player1", 15)
        save_high_score(file_name, "Player2", 10)

        high_score = get_high_score(file_name)
        self.assertEqual(high_score, ("Player2", 10))  # Player2 should have the lowest score

        # Cleanup
        os.remove(file_name)

    def test_display_board(self):
        """
        Test board display output.
        """
        # Mock a small board for testing
        test_board = [[' ' for _ in range(5)] for _ in range(5)]
        test_board[0][0] = 'X'
        test_board[2][2] = 'O'
        test_board[4][4] = 'S'

        # Capture display output
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output
        display_board(test_board, show_ships=True)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("X", output)  # Ensure hit is displayed
        self.assertIn("O", output)  # Ensure miss is displayed
        self.assertIn("S", output)  # Ensure ships are displayed when show_ships=True


if __name__ == "__main__":
    unittest.main()
