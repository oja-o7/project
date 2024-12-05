# project 4 (user interface)
from game_mechanics import ColumnsGame, InvalidColumnError, InvalidFallerError, InvalidJewelsError

def prompt_for_field_size() -> tuple:
    '''
    The function prompts the user for the number of rows and columns and
    returns them as ints.
    '''
    rows = int(input())
    columns = int(input())
    return rows, columns

def prompt_for_field(rows: int, columns: int):
    '''
    The function prompts the user to select a field type
    ('CONTENTS' or 'EMPTY') and returns the corresponding ColumnsGame
    object.
    '''
    
    field = input()
    if field == 'CONTENTS':
        contents = prompt_for_field_contents(rows, columns)
        columns_game = create_board_with_contents(contents, rows, columns)
        return columns_game
    elif field == 'EMPTY':
        columns_game = create_empty_board(rows, columns)
        return columns_game
    else:
        raise ValueError(f"Invalid field input: {field}. Expected 'CONTENTS' or 'EMPTY'.")
        
def prompt_for_field_contents(rows: int, columns: int) -> list[str]:
    '''
    This function prompts the user to input the contents for each row
    of the game board. Returns the input as a list.
    '''
    contents = []
    for r in range(rows):
        field_content = input()
        contents.append(field_content)
    return contents

def create_board_with_contents(contents: list[str], rows, columns) -> ColumnsGame:
    '''
    This function creates a ColumnsGame instance with the specified contents
    and board dimensions. It returns ColumnsGame.
    '''
    columns_game = ColumnsGame(rows, columns)
    columns_game.create_specified_field(contents)
    return columns_game

def create_empty_board(rows: int, columns: int) -> ColumnsGame:
    '''
    This function creates an empty ColumnsGame instance with the specified
    dimensions.
    '''
    columns_game = ColumnsGame(rows, columns)
    return columns_game

def display_board(columns_game_board: 'board') -> str:
    '''
    This function formats the game board for display. It returns the formatted
    board as a list.
    '''
    board_lines = []
    for row in columns_game_board:
        formatted_row = ''.join(cell.center(3) for cell in row)
        board_lines.append(f'|{formatted_row}|')
    board_lines.append(' ' + '-' * (len(columns_game_board[0]) * 3) + ' ')
    return board_lines

def game_loop(columns_game: ColumnsGame) -> None:
    '''
    This function runs the main game loop, processes user commands, and
    updates the game board.
    '''
    columns_game.find_matches()
    
    while not game_is_over(columns_game):
        board_lines = display_board(columns_game._board)
        for line in board_lines:
            print(line)

        command = input().strip()

        if command == 'Q':
            break
        elif command.startswith('F'):
            column = command.split()[1]
            jewels = command.split()[2:]
            columns_game.create_faller(int(column), jewels)
        elif command == 'R':
            columns_game.rotate_faller()
        elif command == '<':
            columns_game.move_current_faller_left()
        elif command == '>':
            columns_game.move_current_faller_right()
        elif command == '':
            if columns_game._matches_marked:
                columns_game.remove_matches()
            else:
                columns_game.find_matches()
                columns_game.update_game()

def game_is_over(columns_game: ColumnsGame) -> bool:
    if columns_game.game_over():
        print('GAME OVER')
        return True
    else:
        return False
    

def run_game() -> None:
    rows, columns = prompt_for_field_size()
    columns_game = prompt_for_field(rows, columns)
    game_loop(columns_game)
    

if __name__ == '__main__':
    run_game()
