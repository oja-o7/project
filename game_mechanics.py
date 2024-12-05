# game_mechanics.py

class InvalidColumnError(Exception):
    pass

class InvalidFallerError(Exception):
    pass
class InvalidJewelsError(Exception):
    pass

class ColumnsGame:
    def __init__(self, rows: int, columns: int):
        self._rows = rows
        self._columns = columns
        self._board = [[' ' for _ in range(columns)] for _ in range(rows)]
        self._current_faller = None
        self._remaining_faller = None
        self._game_over = False
        self._faller_should_freeze = False
        self._matches_marked = False
        self._matches_pending = False


    def _apply_gravity(self, contents_list: list[str]) -> list[str]:
        '''
        This function takes the contents from a game causes the
        cells with jewels to "fall" beneath themselves if there
        are empty spaces. It returns the updated list.
        '''
        rows = [list(row) for row in contents_list]
        cols = list(zip(*rows))

        new_cols = []
        for col in cols:
            non_spaces = [char for char in col if char != ' ']
            spaces = [' '] * (len(col) - len(non_spaces))
            new_cols.append(spaces + non_spaces)

        new_rows = list(zip(*new_cols))
        list_rows = [list(row) for row in new_rows]
        return list_rows
            
        

    def create_specified_field(self, contents: list[str]) -> None:
        '''
        This function takes specified contents from previous user input
        and applies gravity to the cells to make sure all content has
        fallen down. It sets the gamne board to this new content.'
        '''
        self._board = self._apply_gravity(contents)        

    def create_faller(self, column: int, jewels: list[str]) -> None:
        '''
        This function creates a new faller for the game with the
        specified jewels and column. It sets the position or row
        at the top (zero). Additionally, it sets the bottom of the
        faller at the top of the board at the specified column.
        '''
        if self._current_faller is not None:
            raise InvalidFallerError('A faller is already active.')
        if not 1 <= column <= self._columns:
            raise InvalidColumnError('Invalid column number.')
        if len(jewels) != 3:
            raise InvalidJewelsError('A faller must contain exactly 3 jewels.')

        self._current_faller = {'column': column - 1, 'jewels': jewels, 'position': 0}
        self._board[0][column - 1] = f'[{jewels[2]}]'

    def _clear_previous_position(self) -> None:
        '''
        Clear the faller's previous position on the board.
        '''
        if self._current_faller is None:
            return
        
        column = self._current_faller['column']
        for i, jewel in enumerate(self._current_faller['jewels']):
            row = self._current_faller['position'] - i
            if row >= 0:
                self._board[row][column] = ' '

    def _update_new_position(self) -> None:
        '''
        This function places the new current faller's jewels in the correct position
        of the board when the piece falls down. 
        '''
        for i, jewel in enumerate(self._current_faller['jewels'][::-1]):
            row = self._current_faller['position'] - i
            if row >= 0:
                self._board[row][self._current_faller['column']] = f'[{jewel}]'

    def move_current_faller_left(self) -> None:
        '''
        This move the current faller to the left if available. It removes the
        previous postion and updates the game board with the new position. 
        '''
        
        if self._current_faller is None:
            return

        column = self._current_faller['column']

        if self.can_move_to_next_column():
            if column > 0:
                for row in range(len(self._board)):
                    if self._board[row][column - 1] != ' ' and \
                       self._board[row][column - 1] not in self._current_faller['jewels']:
                        return
                
                self._clear_previous_position()

                self._current_faller['column'] -= 1
                for i, jewel in enumerate(self._current_faller['jewels'][::-1]):
                    row = self._current_faller['position'] - i
                    if row >= 0:
                        self._board[row][column - 1] = f'[{jewel}]'
                        
                self._faller_should_freeze = False
        else:
            self.freeze_current_faller()

    def move_current_faller_right(self) -> None:
        '''
        This move the current faller to the right if available. It removes the
        previous postion and updates the game board with the new position. 
        '''
        if self._current_faller is None:
            return

        column = self._current_faller['column']

        if self.can_move_to_next_column():
            if column < len(self._board[0]) - 1:
                for row in range(len(self._board)):
                    if self._board[row][column + 1] != ' ' and \
                       self._board[row][column + 1] not in self._current_faller['jewels']:
                        return
                
                self._clear_previous_position()

                self._current_faller['column'] += 1
                for i, jewel in enumerate(self._current_faller['jewels'][::-1]):
                    row = self._current_faller['position'] - i
                    if row >= 0:
                        self._board[row][column + 1] = f'[{jewel}]'
                        
                self._faller_should_freeze = False
        else:
            self.freeze_current_faller()

    def rotate_faller(self) -> None:
        '''
        This function rotates the jewels vertically in the current faller.
        it updates the new jewels position on the game board.
        '''
        if self._current_faller is None:
            return

        jewels = self._current_faller['jewels']
        self._current_faller['jewels'] = [jewels[2], jewels[0], jewels[1]]
        self._update_new_position()

    def _is_current_faller_landed(self) -> bool:
        '''
        Check if the faller has landed by inspecting the bottom.
        '''
        if self._current_faller:
            column = self._current_faller['column']
            position = self._current_faller['position']  

            if position + 1 >= self._rows:
                return True
            if self._board[position + 1][column] != ' ':
                return True

            return False

    def can_move_to_next_column(self) -> bool:
        '''
        Check if the faller can move to the next column (either left or right).
        '''
        if self._current_faller is None:
            return False

        position = self._current_faller['position']
        column = self._current_faller['column']

        if column + 1 < self._columns:  
            if position + 1 < self._rows and self._board[position + 1][column + 1] == ' ':
                return True  

        if column - 1 >= 0:  
            if position + 1 < self._rows and self._board[position + 1][column - 1] == ' ':
                return True  
        return False 
   
    def update_game(self) -> None:
        '''
        Updates the game state. If there are any marked matches, they are removed.
        If a faller has landed, it checks if it fits, and moves the remaining faller down if necessary.
        '''
        # Check if there's a remaining faller and let it fall
        if self._remaining_faller:
            column = self._remaining_faller['column']
            jewels = self._remaining_faller['jewels']
            position = self._get_faller_fall_position(column, jewels)

            if position is not None:
                self._remaining_faller['position'] = position
                self._update_new_position()  
                self._remaining_faller = None  

            # Game ends if the faller can't fit
            else:
                self._game_over = True  

        elif self._is_current_faller_landed():
            if self._faller_should_freeze:
                self.freeze_current_faller()
            elif self.can_move_to_next_column():
                self.postpone_freeze()
            else:
                self.freeze_current_faller()
        else:
            self._clear_previous_position()
            self._current_faller['position'] += 1
            self._update_new_position()
            self._faller_should_freeze = False
            if not self._matches_marked:
                self.current_faller_change_jewel_if_fallen()
                

        # Handle matches if any are marked
        if self._matches_marked:
            self._matches_pending = True

    def current_faller_change_jewel_if_fallen(self) -> None:
        position = self._current_faller['position']
        column = self._current_faller['column']
        if position + 1 >= self._rows or self._board[position + 1][column] != ' ':
            for i, jewel in enumerate(self._current_faller['jewels'][::-1]):
                row = self._current_faller['position'] - i
                if row >= 0:
                    self._board[row][column] = f'|{jewel}|'
            

    def freeze_current_faller(self) -> None:
        '''
        Freeze the current faller by converting its jewels to a frozen state.
        If matches exist, delay game-over conditions and handle remaining jewels.
        '''
        column = self._current_faller['column']
        remaining_jewels = []

        # Freeze jewels on the board or collect remaining jewels outside the board
        for i, jewel in enumerate(self._current_faller['jewels'][::-1]):
            row = self._current_faller['position'] - i
            if row >= 0:
                self._board[row][column] = jewel
            else:
                remaining_jewels.append(jewel)

        # Check for matches
        self.find_matches()
        if self._matches_marked:

            # Reintroduce remaining jewels as a new faller if space is available
            if remaining_jewels:
                self._remaining_faller = {'column': column, 'jewels': remaining_jewels[::-1], 'position': -len(remaining_jewels)}
            else:
                self._remaining_faller = None

        elif not self._check_if_faller_fits_on_board():
            self._game_over = True  # Game over if faller doesn't fit
            
        self._current_faller = None
        self._faller_should_freeze = False


    def postpone_freeze(self) -> bool:
        '''
        This function prompts for the next blank line input to cause the function to
        freeze if there are no available spots to move.
        '''
        self._faller_should_freeze = True
        

    def _check_if_faller_fits_on_board(self) -> bool:
        '''
        This function checks if the faller fits entirely on the board. The faller is
        valid if all jewels are within the board's rows and columns.
        '''
        if self._current_faller is None:
            return True  
    
        column = self._current_faller['column']
        position = self._current_faller['position']
        jewels = self._current_faller['jewels'][::-1]

        for i, jewel in enumerate(jewels):
            row = position - i
            if row < 0 or row >= self._rows:  
                return False
            if column < 0 or column >= self._columns:  
                return False

        return True

    def game_over(self) -> bool:
        '''
        This function determines if the game is over. The game ends if the
        remaining jewels exist after freezing with no matches or the board
        is full and no faller exists.
        '''
        # Game over if remaining jewels exist after a freeze with no matches
        if self._remaining_faller is not None:
            return False  

        # Game over if board is full and no faller exists
        if all(self._board[0][col] != ' ' for col in range(self._columns)):
            return True

        if self._game_over:
            return self._game_over

        return False
    
    def find_matches(self) -> None:
        '''
        The function finds all matching sequences (horizontal, vertical, diagonal)
        on the board. Marks matches with `*` and sets `_matches_marked` to True
        if any are found.
        '''
        matches = set()  # Use a set to avoid duplicate coordinates

        # Horizontal matches
        for row in range(self._rows):
            for col in range(self._columns - 2):
                if self._board[row][col] != ' ' and '*' not in self._board[row][col] and \
                   self._board[row][col] == self._board[row][col + 1] == self._board[row][col + 2]:
                    matches.update({(row, col), (row, col + 1), (row, col + 2)})

        # Vertical matches
        for col in range(self._columns):
            for row in range(self._rows - 2):
                if self._board[row][col] != ' ' and '*' not in self._board[row][col] and \
                   self._board[row][col] == self._board[row + 1][col] == self._board[row + 2][col]:
                    matches.update({(row, col), (row + 1, col), (row + 2, col)})

        # Diagonal matches (down-right)
        for row in range(self._rows - 2):
            for col in range(self._columns - 2):
                if self._board[row][col] != ' ' and '*' not in self._board[row][col] and \
                   self._board[row][col] == self._board[row + 1][col + 1] == self._board[row + 2][col + 2]:
                    matches.update({(row, col), (row + 1, col + 1), (row + 2, col + 2)})

        # Diagonal matches (up-right)
        for row in range(2, self._rows):
            for col in range(self._columns - 2):
                if self._board[row][col] != ' ' and '*' not in self._board[row][col] and \
                   self._board[row][col] == self._board[row - 1][col + 1] == self._board[row - 2][col + 2]:
                    matches.update({(row, col), (row - 1, col + 1), (row - 2, col + 2)})

        # Mark matches for removal
        for row, col in matches:
            self._board[row][col] = f'*{self._board[row][col]}*'

        self._matches_marked = bool(matches)



    def remove_matches(self) -> None:
        '''
        Removes jewels at the specified coordinates (marked by `*`) and applies gravity to the board.
        '''  
        # Remove jewels marked with `*` by replacing them with spaces
        for row in range(self._rows):
            for col in range(self._columns):
                if '*' in self._board[row][col]:
                    self._board[row][col] = ' '  

        if self._remaining_faller:
            column = self._remaining_faller['column']
            jewels = self._remaining_faller['jewels']

            # Place the remaining faller at the top of the column
            for i, jewel in enumerate(jewels[::-1]):
                row = 0 + i  # Place the faller jewels starting from the top
                if row < self._rows:
                    self._board[row][column] = jewel
            

        # Apply gravity to let jewels above fall down
        self._board = self._apply_gravity([''.join(row) for row in self._board])

        self._remaining_faller = None
        self._matches_marked = False
        self.find_matches()

    def _get_faller_fall_position(self, column: int, jewels: list) -> int:
        '''
        This method calculates the position where the faller should land in a given column.
        It returns the row where the faller should be placed, or None if the faller doesn't fit.
        '''
        # Start from the bottom row
        for row in range(self._rows - 1, -1, -1):  
            if self._board[row][column] == ' ':
                # Check if there's space below for all jewels
                if row - len(jewels) + 1 >= 0:  
                    return row - len(jewels) + 1
        return None  


        

        
