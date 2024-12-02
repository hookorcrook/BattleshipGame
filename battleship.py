from board import initialize_board, display_board
from validator import place_ship, validate_position
from highscores import save_high_score, get_high_score


def get_player_names():
    #Prompt players to enter their names.
    
    print("\nWelcome to Battleship!")
    print("Get ready for an exciting game of strategy and precision.")
    print("Each player will place their ships and take turns guessing enemy ship locations.")
    print("The goal is to sink all enemy ships before your own fleet is destroyed!\n")
    
    player1 = input("Player 1, please enter your name: ")
    player2 = input("Player 2, please enter your name: ")
    print(f"\nWelcome {player1} and {player2}! Let the battle begin!")
    return player1, player2


def setup_ships(player_name, board, ships):
    """
    Allows a player to place their ships on the board.
    """
    print(f"\n{player_name}, it's time to place your ships.")
    for ship_name, ship_size in ships:
        placed = False
        while not placed:
            try:
                print(f"\nPlacing your {ship_name} (Size: {ship_size}):")
                position = input("Enter the center position of the ship (e.g., 'A5'): ").upper()
                alignment = input("Enter the alignment (H for Horizontal, V for Vertical): ").upper()

                row, col = ord(position[0]) - ord('A'), int(position[1:])
                if validate_position(board, ship_size, (row, col), alignment):
                    place_ship(board, ship_size, (row, col), alignment)
                    display_board(board, show_ships=True)
                    placed = True
                else:
                    print("Invalid placement. Try again.")
            except Exception as e:
                print(f"Error: {e}. Please try again.")

    print(f"{player_name}, your ships are set up!")
    display_board(board, show_ships=True)


def play_game(player1, player2, board1, board2, ships):
    """
    Run the main game loop where players take turns guessing.
    """
    print("\nThe game begins!")
    print("{player1} will start guessing.\n")
    turn = 1
    guess_boards = [initialize_board(), initialize_board()]  # To track guesses for each player
    boards = [board1, board2]
    players = [player1, player2]
    sunk_ships = [{name: 0 for name, _ in ships} for _ in range(2)]
    max_hits = sum(size for _, size in ships)

    while True:
        active_player = turn % 2
        opponent = 1 - active_player
        print(f"\n{players[active_player]}'s Turn!")
        display_board(guess_boards[active_player], show_ships=False)
        
        try:
            guess = input("Enter your guess (e.g., 'A5'): ").upper()
            row, col = ord(guess[0]) - ord('A'), int(guess[1:])
            if guess_boards[active_player][row][col] != ' ':
                print("You already guessed that location. Try again.")
                continue

            if boards[opponent][row][col] == 'S':
                print("HIT!")
                guess_boards[active_player][row][col] = 'X'
                boards[opponent][row][col] = 'X'

                # Check if a ship is sunk
                for name, size in ships:
                    hits = sum(
                        1 for r in range(26) for c in range(10)
                        if boards[opponent][r][c] == 'X'
                    )
                    if hits == size and sunk_ships[opponent][name] == 0:
                        sunk_ships[opponent][name] = 1
                        print(f"You sunk {players[opponent]}'s {name}!")
            else:
                print("MISS!")
                guess_boards[active_player][row][col] = 'O'
                boards[opponent][row][col] = 'O'

            # Check for game over
            total_hits = sum(
                sum(1 for cell in row if cell == 'X') for row in boards[opponent]
            )
            if total_hits == max_hits:
                print(f"\nGame Over! {players[active_player]} wins!")
                print(f"Final Boards:")
                print(f"\n{player1}'s Board:")
                display_board(board1, show_ships=True)
                print(f"\n{player2}'s Board:")
                display_board(board2, show_ships=True)

                # Save game stats
                save_high_score("highscores.txt", players[active_player], turn)
                winner, score = get_high_score("highscores.txt")
                print(f"Current High Score: {winner} with {score} guesses.\n")
                return

            turn += 1

        except Exception as e:
            print(f"Error: {e}. Please try again.")


def main():
    """
    Main function to start and manage the game.
    """
    player1, player2 = get_player_names()
    board1 = initialize_board()
    board2 = initialize_board()

    ships = [
        ("Destroyer", 3),
        ("Destroyer", 3),
        ("Cruiser", 5),
        ("Battleship", 7),
        ("Aircraft Carrier", 9),
    ]

    setup_ships(player1, board1, ships)
    setup_ships(player2, board2, ships)

    start = input("\nReady to start the game? (Y/N): ").upper()
    if start == 'Y':
        play_game(player1, player2, board1, board2, ships)
    else:
        print("Exiting the game. Hope you enjoyed it!")


if __name__ == "__main__":
    main()
