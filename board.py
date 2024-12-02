def initialize_board(rows=26, cols=10):
    """
    Initializes an empty game board.
    Args:
        rows: Number of rows (default 26, A-Z).
        cols: Number of columns (default 10).

    Returns:
        list: A 2D list representing the board with all cells initialized as empty (' ').
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def display_board(board, show_ships=False):
    """
    Displays the board in a formatted manner.
    Args:
        board: The player's board as a 2D list.
        show_ships: Boolean indicating whether to display the ships ('S').

    Returns:
        None
    """
    print("   " + " ".join(str(c) for c in range(len(board[0]))))
    for i, row in enumerate(board):
        row_display = "".join(cell if (cell != 'S' or show_ships) else ' ' for cell in row)
        print(f"{chr(i + 65)}  " + " ".join(row_display))


def update_board(board, row, col, marker):
    """
    Updates a cell on the board with a specific marker.
    Args:
        board: The player's board as a 2D list.
        row: Row index.
        col: Column index.
        marker: The marker to place ('X' for hit, 'O' for miss).

    Returns:
        None
    """
    board[row][col] = marker
