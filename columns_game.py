# columns_game.py

import columns
import pygame
import random

_FRAME_RATE = 30
_INITIAL_WIDTH = 600
_INITIAL_HEIGHT = 600
_TICK_INTERVAL = 800
_BACKGROUND_COLOR = pygame.Color(0, 0, 0)
_JEWELS_COLORS = {
    'S': pygame.Color(255, 0, 0),    # Red
    'T': pygame.Color(0, 255, 0),    # Green
    'V': pygame.Color(0, 0, 255),    # Blue
    'W': pygame.Color(255, 255, 0),  # Yellow
    'X': pygame.Color(255, 165, 0),  # Orange
    'Y': pygame.Color(128, 0, 128),  # Purple
    'Z': pygame.Color(0, 255, 255)   # Cyan
}

class Columns:
    def __init__(self):
        self._state = columns.GameState()
        self._running = True
        self._last_tick_time = 0

    def run(self) -> None:
        pygame.init()

        try:
            clock = pygame.time.Clock()

            self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))

            while self._running:
                clock.tick(_FRAME_RATE)
                self._handle_events()
                self._draw_frame()

        finally:
            pygame.quit()

    def _create_surface(self, size: tuple[int, int]) -> None:
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            self._handle_event(event)
                

    def _handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.VIDEORESIZE:
            self._create_surface(event.size)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._state.current_faller().rotate()
            elif event.key == pygame.K_LEFT:
                self._state.current_faller().move_left()
            elif event.key == pygame.K_RIGHT:
                self._state.current_faller().move_right()


    def _stop_running(self) -> None:
        self._running = False

    def _draw_frame(self) -> None:
        self._surface.fill(_BACKGROUND_COLOR)
        
        current_time = pygame.time.get_ticks()
        if current_time - self._last_tick_time >= _TICK_INTERVAL:
            self._create_current_faller()
            if self._state.current_faller().columns_game()._matches_marked:
                self._state.current_faller().remove_matching_jewels()
            else:
                self._state.current_faller().find_matching_jewels()
                self._state.current_faller().update_game_board()
            self._last_tick_time = current_time
        self._draw_board()

        pygame.display.flip()
        

    def _create_current_faller(self) -> None:
        if self._state.current_faller().columns_game()._current_faller is None:
            # Randomly select three colors (can include duplicates)
            first_letter = random.choice(list(_JEWELS_COLORS.keys()))
            second_letter = random.choice(list(_JEWELS_COLORS.keys()))
            if second_letter == first_letter:
                third_letter = random.choice(
                    [color for color in _JEWELS_COLORS.keys() if color != second_letter]
                )
            else:
                third_letter = random.choice(list(_JEWELS_COLORS.keys()))

            selected_letters = list((first_letter, second_letter, third_letter))
            self._state.current_faller().create_new_faller(selected_letters)
    

    def _draw_board(self) -> None:
        # Get the game board from the state
        board = self._state.current_faller().columns_game()._board
        for line in board:
            print(line)

        # Calculate cell dimensions
        width_pixel = self._frac_x_to_pixel_x(1.0 / self._state.current_faller().columns_game()._columns)
        height_pixel = self._frac_y_to_pixel_y(1.0 / self._state.current_faller().columns_game()._rows)

        # Iterate through the rows and columns of the board
        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                top_left_pixel_x = col_index * width_pixel
                top_left_pixel_y = row_index * height_pixel

                # Determine the color or empty space
                if cell.strip('[]*|') in _JEWELS_COLORS:  # Check if the cell is a jewel

                    color = _JEWELS_COLORS[cell.strip('[]*|')]
                    pygame.draw.rect(
                        self._surface,
                        color,
                        pygame.Rect(top_left_pixel_x, top_left_pixel_y, width_pixel, height_pixel)
                    )
                else:
                    # Optionally, draw an empty space or leave it as the background
                    pygame.draw.rect(
                        self._surface,
                        _BACKGROUND_COLOR,
                        pygame.Rect(top_left_pixel_x, top_left_pixel_y, width_pixel, height_pixel)
                    )



    def _frac_x_to_pixel_x(self, frac_x: float) -> int:
        return self._frac_to_pixel(frac_x, self._surface.get_width())


    def _frac_y_to_pixel_y(self, frac_y: float) -> int:
        return self._frac_to_pixel(frac_y, self._surface.get_height())


    def _frac_to_pixel(self, frac: float, max_pixel: int) -> int:
        return int(frac * max_pixel)


if __name__ == '__main__':
    Columns().run()

    
