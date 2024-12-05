# project 4 testing

from game_mechanics import *
from project4 import *
import unittest

class GameMechanicsTest(unittest.TestCase):
    def setUp(self):
        self._game = ColumnsGame(4, 4)

    def test_create_empty_field_of_the_correct_size(self):
        expected_board = [
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]
        self.assertEqual(self._game._board, expected_board)

    def test_create_field_of_specified_contents_with_jewels_in_some_cells(self):
        self._game.create_specified_field([' Y X', 'S V ', 'TXYS', 'X XY'])
        expected_board = [
            [' ', ' ', ' ', ' '],
            ['S', ' ', 'V', 'X'],
            ['T', 'Y', 'Y', 'S'],
            ['X', 'X', 'X', 'Y']
        ]
        self.assertEqual(self._game._board, expected_board)
        
    def test_create_faller_at_top(self):
        self._game.create_faller(2, ['X', 'Y', 'Z'])
        expected_board = [
            [' ', '[Z]', ' ', ' '],  
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]
        self.assertEqual(self._game._board, expected_board)
        self.assertEqual(self._game._current_faller, {'column': 1, 'jewels': ['X', 'Y', 'Z'], 'position': 0})

    def test_move_a_newly_created_current_faller_left(self):
        self._game.create_faller(2, ['X', 'Y', 'Z'])
        self._game.move_current_faller_left()
        expected_board = [
            ['[Z]', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]
        self.assertEqual(self._game._board, expected_board)

    def test_move_a_newly_created_current_faller_blocked_by_left_bounds(self):
        self._game.create_faller(1, ['X', 'Y', 'Z'])
        self._game.move_current_faller_left()
        self._game.move_current_faller_left()
        self._game.move_current_faller_left()
        expected_board = [
            ['[Z]', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]
        self.assertEqual(self._game._board, expected_board)

    def test_move_a_newly_created_current_faller_blocked_by_right_bounds(self):
        self._game.create_faller(3, ['X', 'Y', 'Z'])
        self._game.move_current_faller_right()
        self._game.move_current_faller_right()
        self._game.move_current_faller_right()
        expected_board = [
            [' ', ' ', ' ', '[Z]'],  
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]
        self.assertEqual(self._game._board, expected_board)
        
    def test_move_a_newly_created_current_faller_right(self):
        self._game.create_faller(2, ['X', 'Y', 'Z'])
        self._game.move_current_faller_right()
        expected_board = [
            [' ', ' ', '[Z]', ' '],  
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]
        self.assertEqual(self._game._board, expected_board)

    def test_move_current_faller_to_the_right_two_times(self):
        self._game.create_faller(1, ['X', 'Y', 'Z'])
        self._game.move_current_faller_right()
        self._game.move_current_faller_right()
        expected_board = [
            [' ', ' ', '[Z]', ' '],  
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]
        self.assertEqual(self._game._board, expected_board)

    def test_move_current_faller_to_the_left_two_times(self):
        self._game.create_faller(3, ['X', 'Y', 'Z'])
        self._game.move_current_faller_left()
        self._game.move_current_faller_left()
        expected_board = [
            ['[Z]', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]
        self.assertEqual(self._game._board, expected_board)

    def test_move_a_current_faller_with_two_jewels_visible_to_the_left(self):
        self._game.create_faller(3, ['Y', 'Z', 'X'])

        self._game._current_faller['position'] = 1
        self._game._board[0][2] = '[Z]'
        self._game._board[1][2] = '[X]'

        expected_board = [
            [' ', ' ', '[Z]', ' '],  
            [' ', ' ', '[X]', ' '],  
            [' ', ' ', ' ', ' '],    
            [' ', ' ', ' ', ' ']     
        ]
        self.assertEqual(self._game._board, expected_board)

        self._game.move_current_faller_left()

        expected_board = [
            [' ', '[Z]', ' ', ' '],  
            [' ', '[X]', ' ', ' '],  
            [' ', ' ', ' ', ' '],    
            [' ', ' ', ' ', ' ']     
        ]
        self.assertEqual(self._game._board, expected_board)

    def test_move_a_current_faller_with_two_jewels_visible_to_the_right(self):
        self._game.create_faller(3, ['Y', 'Z', 'X'])

        self._game._current_faller['position'] = 1
        self._game._board[0][2] = '[Z]'
        self._game._board[1][2] = '[X]'

        expected_board = [
            [' ', ' ', '[Z]', ' '],  
            [' ', ' ', '[X]', ' '],  
            [' ', ' ', ' ', ' '],    
            [' ', ' ', ' ', ' ']     
        ]
        self.assertEqual(self._game._board, expected_board)

        self._game.move_current_faller_right()

        expected_board = [
            [' ', ' ', ' ', '[Z]'],  
            [' ', ' ', ' ', '[X]'],  
            [' ', ' ', ' ', ' '],    
            [' ', ' ', ' ', ' ']     
        ]
        self.assertEqual(self._game._board, expected_board)

    def test_bool_state_for_is_current_faller_landed_if_in_midair_is_false(self):
        self._game._current_faller = {'column': 1, 'jewels': ['X', 'Y', 'Z'], 'position': 2}
        self._game._board[3][1] = ' '
        self.assertFalse(self._game._is_current_faller_landed())

    def test_bool_state_for_is_current_faller_landed_if_at_bottom_is_true(self):
        self._game._current_faller = {'column': 1, 'jewels': ['X', 'Y', 'Z'], 'position': 3}
        self.assertTrue(self._game._is_current_faller_landed())

    def test_bool_state_for_is_current_faller_landed_if_on_a_frozen_jewel(self):
        self._game._current_faller = {'column': 1, 'jewels': ['X', 'Y', 'Z'], 'position': 2}
        self._game._board[3][1] = 'X'
        self.assertTrue(self._game._is_current_faller_landed())

    def test_update_game_makes_current_faller_fall_down(self):
        self._game._current_faller = {'column': 1, 'jewels': ['X', 'Y', 'Z'], 'position': 0}
        self._game.update_game()
        self.assertEqual(self._game._current_faller['position'], 1)
        self.assertEqual(self._game._board[1][1], '[Z]')
        self.assertEqual(self._game._board[0][1], '[Y]')       

    def test_update_game_calls_freeze_when_landed(self):
        self._game._current_faller = {'column': 1, 'jewels': ['X', 'Y', 'Z'], 'position': 3}
        self._game.update_game()
        self.assertEqual(self._game._current_faller, None)
        self.assertEqual(self._game._board[3][1], 'Z')
        self.assertEqual(self._game._board[2][1], 'Y')
        self.assertEqual(self._game._board[1][1], 'X')

    def test_update_game_postpone_freeze_if_columns_adjacent_are_empty_the_row_below_is_true(self):
        self._game._current_faller = {'column': 1, 'jewels': ['X', 'Y', 'Z'], 'position': 2}
        self._game._board[3][1] = 'X'
        self._game.update_game()
        self.assertTrue(self._game.can_move_to_next_left_column())

    def test_update_game_postpone_freeze_if_there_are_no_columns_adjacent_that_are_empty_is_false(self):
        self._game._current_faller = {'column': 1, 'jewels': ['X', 'Y', 'Z'], 'position': 3}
        self._game.update_game()
        self.assertFalse(self._game.can_move_to_next_left_column())
        
    def test_freeze_current_faller(self):
        self._game._current_faller = {'column': 2, 'jewels': ['X', 'Y', 'Z'], 'position': 3}
        self._game._board[3][2] = '[Z]'
        self._game._board[2][2] = '[Y]'
        self._game._board[1][2] = '[X]'

        self._game.freeze_current_faller()

        self.assertEqual(self._game._board[3][2], 'Z')
        self.assertEqual(self._game._board[2][2], 'Y')
        self.assertEqual(self._game._board[1][2], 'X')

    def test_rotate_current_faller(self):
        self._game._current_faller = {'column': 3, 'jewels': ['X', 'Y', 'Z'], 'position': 0}
        self._game.rotate_faller()
        expected_result = {'column': 3, 'jewels': ['Z', 'X', 'Y'], 'position': 0}
        self.assertEqual(self._game._current_faller, expected_result)
        

    def test_rotate_current_faller_before_frozen(self):
        self._game._current_faller = {'column': 1, 'jewels': ['X', 'Y', 'Z'], 'position': 2}
        self._game.update_game()
        self._game.rotate_faller()
        expected_result = {'column': 1, 'jewels': ['Z', 'X', 'Y'], 'position': 3}
        self.assertEqual(self._game._current_faller, expected_result)

    def test_current_faller_stop_falling_changes_jewels_in_board_to_have_parallel_lines_around_it(self):
        self._game.create_faller(4, ['Y', 'Z', 'X'])
        self._game.update_game()
        self._game.update_game()
        self._game.update_game()
        expected_board = [
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', '|Y|'],  
            [' ', ' ', ' ', '|Z|'],    
            [' ', ' ', ' ', '|X|']     
        ]
        self.assertEqual(self._game._board, expected_board)

    def test_matching_jewels_have_asterisk_around_them(self):
        self._game._board = [
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', 'X'],  
            [' ', ' ', ' ', 'X'],    
            [' ', ' ', ' ', 'X']     
        ]
        self._game.find_matches()
        expected_board = [
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', '*X*'],  
            [' ', ' ', ' ', '*X*'],    
            [' ', ' ', ' ', '*X*']     
        ]

        self.assertEqual(self._game._board, expected_board)

    def test_diagonal_matching_jewels_up_right(self):
        self._game._board = [
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', 'X'],  
            [' ', ' ', 'X', ' '],    
            [' ', 'X', ' ', ' ']     
        ]
        self._game.find_matches()
        expected_board = [
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', '*X*'],  
            [' ', ' ', '*X*', ' '],    
            [' ', '*X*', ' ', ' ']     
        ]
        self.assertEqual(self._game._board, expected_board)
        
    def test_horizontal_matching_jewels(self):
        self._game._board = [
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],    
            [' ', 'X', 'X', 'X']     
        ]
        self._game.find_matches()
        expected_board = [
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],    
            [' ', '*X*', '*X*', '*X*']     
        ]
        self.assertEqual(self._game._board, expected_board)

    def test_diagonal_matching_jewels_down_right(self):
        self._game._board = [
            [' ', ' ', ' ', ' '],  
            [' ', 'X', ' ', ' '],  
            [' ', ' ', 'X', ' '],    
            [' ', ' ', ' ', 'X']     
        ]
        self._game.find_matches()
        expected_board = [
            [' ', ' ', ' ', ' '],  
            [' ', '*X*', ' ', ' '],  
            [' ', ' ', '*X*', ' '],    
            [' ', ' ', ' ', '*X*']     
        ]
        self.assertEqual(self._game._board, expected_board)


    def test_freeze_outside_of_the_box_results_in_game_over(self):
        self._game.create_faller(2, ['X', 'Y', 'Z'])
        self._game.freeze_current_faller()
        self.assertTrue(self._game._game_over)

    def test_remove_matches(self):
        self._game._board = [
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],    
            [' ', '*X*', '*X*', '*X*']     
        ]
        self._game.remove_matches()
        expected_board = [
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],  
            [' ', ' ', ' ', ' '],    
            [' ', ' ', ' ', ' ']     
        ]
        self.assertEqual(self._game._board, expected_board)


class Project4Test(unittest.TestCase):
    def setUp(self):
        self._game = ColumnsGame(4, 3)

    def test_display_board(self):
        self._game._board = [["S", "X", "X"], ["T", "Y", "Y"], ["Z", "Z", "Z"]]
        expected_output = [
            "| S  X  X |",
            "| T  Y  Y |",
            "| Z  Z  Z |",
            " --------- "
        ]
        board = display_board(self._game._board)
        self.assertEqual(board, expected_output)

if __name__ == '__main__':
    unittest.main()
