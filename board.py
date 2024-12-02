#Size of the board
ROWS = 26, COLS = 10;

#Default Size is 26 (rows A-Z) and 10 columns.

def initialize_board(rows=ROWS, cols=COLS):

    ##Returns a 2D list representing the board with all cells initialized as empty (' ').
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def display_board(board, show_ships=False):
    #Display the player's board as a 2D list. Boolean indicating whether to display the ships ('S').
    print("   " + " ".join(str(c) for c in range(len(board[0]))))
    for i, row in enumerate(board):
        row_display = "".join(cell if (cell != 'S' or show_ships) else ' ' for cell in row)
        print(f"{chr(i + 65)}  " + " ".join(row_display))


def update_board(board, row, col, marker):
    """
    Updates a cell on the board with a specific marker after each turn.
    Params:
        board: 2D list.
        row: Row index.
        col: Column index.
        marker: The marker to place ('X' for hit, 'O' for miss).
    """
    board[row][col] = marker
