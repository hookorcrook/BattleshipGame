def validate_position(board, ship_length, anchor, alignment):
    """
    Validates whether a ship can be placed on the board at the given position and alignment.
    Args:
        board: The player's board as a 2D list.
        ship_length: Length of the ship.
        anchor: (row, col) tuple indicating the middle point of the ship.
        alignment: 'H' for horizontal, 'V' for vertical.

    Returns:
        bool: True if the position is valid, False otherwise.
    """
    rows, cols = len(board), len(board[0])
    row, col = anchor
    half_length = ship_length // 2

    if alignment == 'H':
        start_col = col - half_length
        end_col = col + half_length
        if start_col < 0 or end_col >= cols:  # Check bounds
            return False
        if any(board[row][c] != ' ' for c in range(start_col, end_col + 1)):  # Check overlap
            return False
    elif alignment == 'V':
        start_row = row - half_length
        end_row = row + half_length
        if start_row < 0 or end_row >= rows:  # Check bounds
            return False
        if any(board[r][col] != ' ' for r in range(start_row, end_row + 1)):  # Check overlap
            return False
    else:
        return False  # Invalid alignment

    return True


def place_ship(board, ship_length, anchor, alignment):
    """
    Places a ship on the board if the position is valid.
    Args:
        board: The player's board as a 2D list.
        ship_length: Length of the ship.
        anchor: (row, col) tuple indicating the middle point of the ship.
        alignment: 'H' for horizontal, 'V' for vertical.

    Returns:
        bool: True if the ship was placed successfully, False otherwise.
    """
    if not validate_position(board, ship_length, anchor, alignment):
        return False

    row, col = anchor
    half_length = ship_length // 2

    if alignment == 'H':
        for c in range(col - half_length, col + half_length + 1):
            board[row][c] = 'S'
    elif alignment == 'V':
        for r in range(row - half_length, row + half_length + 1):
            board[r][col] = 'S'

    return True
