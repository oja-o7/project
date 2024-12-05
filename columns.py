# columns.py

from game_mechanics import ColumnsGame, InvalidColumnError, InvalidFallerError, InvalidJewelsError
import random




class CurrentFaller:
    def __init__(self):
        self._columns_game = ColumnsGame(13, 6)
        num_columns = 6
        column_width = 1.0 / num_columns
        self._faller_width = column_width
        self._faller_height = 3.0 / 13
        self._columns_index = random.randint(0, num_columns - 1)
        center_x = (self._columns_index + 0.5) * column_width
        top_left_x = center_x - self._faller_width / 2
        top_left_y = 0
        self._top_left = (top_left_x, top_left_y)
        

    def columns_game(self):
        return self._columns_game

    def columns_index(self):
        return self._columns_index

    def top_left(self) -> tuple[float, float]:
        return self._top_left

    def width(self) -> float:
        return self._faller_width

    def height(self) -> float:
        return self._faller_height

    def create_new_faller(self, jewels: list[str]) -> int:
        column = self.columns_index() + 1
        self.columns_game().create_faller(column, jewels)

    def move_left(self) -> None:
        self.columns_game().move_current_faller_left()

    def move_right(self) -> None:
        self.columns_game().move_current_faller_right()

    def rotate(self) -> None:
        self.columns_game().rotate_faller()

    def update_game_board(self) -> None:
        self.columns_game().update_game()

    def find_matching_jewels(self) -> None:
        self.columns_game().find_matches()

    def remove_matching_jewels(self) -> None:
        self.columns_game().remove_matches()

class GameState:
    def __init__(self):
        self._current_faller = CurrentFaller()

    def current_faller(self) -> CurrentFaller:
        return self._current_faller
    
