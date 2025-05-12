import unittest
from unittest.mock import patch, MagicMock
from game import Game
from Constants import GAME_INSTRUCTIONS

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_initial_state(self):
        self.assertFalse(self.game.game_over)
        self.assertIsNotNone(self.game.grid)

    @patch('builtins.print')
    def test_show_instructions(self, mock_print):
        self.game.show_instructions()
        mock_print.assert_called_with(GAME_INSTRUCTIONS)  # Replace with actual GAME_INSTRUCTIONS if needed

    @patch('builtins.input', side_effect=["HELP", "Q"])
    @patch('builtins.print')
    def test_play_game_help_and_quit(self, mock_print, mock_input):
        self.game.play_game()
        self.assertTrue(self.game.game_over)
        mock_print.assert_any_call(GAME_INSTRUCTIONS)  # Replace as needed
        mock_print.assert_any_call("Quitting game.")

    @patch('builtins.input', side_effect=["S"])
    def test_play_game_show_solution(self, mock_input):
        self.game.grid.reveal_mines = MagicMock()
        self.game.play_game()
        self.assertTrue(self.game.game_over)
        self.game.grid.reveal_mines.assert_called_once()

    @patch('builtins.input', side_effect=["Z9", "Q"])
    @patch('builtins.print')
    def test_play_game_invalid_input(self, mock_print, mock_input):
        self.game.play_game()
        mock_print.assert_any_call("Invalid input.")

    @patch('game.label_to_coord_and_dir')
    @patch('game.Ray')
    @patch('builtins.input', side_effect=["A", "Q"])
    @patch('builtins.print')
    def test_trace_ray_valid(self, mock_print, mock_input, mock_ray_class, mock_label_to_coord_and_dir):
        mock_label_to_coord_and_dir.return_value = ((0, 0), (0, 1))
        mock_ray = MagicMock()
        mock_ray.move.return_value = "exit"
        mock_ray_class.return_value = mock_ray

        self.game.play_game()

        mock_ray.move.assert_called_once()
        mock_print.assert_any_call("A → exit")

    @patch('game.label_to_coord_and_dir', return_value=(None, None))
    @patch('builtins.print')
    def test_trace_ray_invalid_label(self, mock_print, mock_label):
        self.game.trace_ray("Z")
        mock_print.assert_called_with("Invalid entry label.")

    @patch('builtins.print')
    def test_guess_atom(self, mock_print):
        self.game.grid.grid = [[None for _ in range(8)] for _ in range(8)]
        self.game.guess_atom("A1")
        self.assertEqual(self.game.grid.grid[0][1], "?")
        mock_print.assert_called_with("Marked A1 as guessed atom.")

    @patch('builtins.print')
    def test_unmark_guess_atom(self, mock_print):
        self.game.grid.grid = [[None for _ in range(8)] for _ in range(8)]
        self.game.guess_atom("A1")
        self.assertEqual(self.game.grid.grid[0][1], "?")
        self.game.guess_atom("A1")
        self.assertEqual(self.game.grid.grid[0][1], "")
        mock_print.assert_called_with("Unmarked A1 as guessed atom.")

if __name__ == '__main__':
    unittest.main()
