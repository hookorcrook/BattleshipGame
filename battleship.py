from board import initialize_board, display_board
from validator import place_ship, validate_position
from highscores import save_high_score, get_high_score


def get_player_names():
    #Ask players to enter their names.
    print("\nWelcome to Battleship!")
    print("Get ready for an exciting game of strategy and precision.")
    print("Each player will place their ships and take turns guessing enemy ship locations.")
    print("The goal is to sink all enemy ships before your own fleet is destroyed!\n")
    
    player1 = input("Player 1, please enter your name: ")
    player2 = input("Player 2, please enter your name: ")
    print(f"\nWelcome {player1} and {player2}! Let the battle begin!")
    return player1, player2


def setup_ships(player_name, board, ships):
    #Lets the players to place their ships on the board.
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


def play_game(player1, player2, board1, board2, ships1, ships2):
    print("\nLet the battle begin!")
    print("Player 1: {player1} will start guessing.\n")
    turn = 1
    guess_boards = [initialize_board(), initialize_board()]  # To track guesses for each player
    boards = [board1, board2]
    ship_data = [ships1, ships2]
    players = [player1, player2]

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

                # Check which ship was hit
                for ship_name, data in ship_data[opponent].items():
                    if (row, col) in data["positions"]:
                        data["hits"] += 1
                        if data["hits"] == data["size"]:
                            print(f"SHIP SUNK! \n You sunk {players[opponent]}'s {ship_name}!")
                        break
            else:
                print("MISS!")
                guess_boards[active_player][row][col] = 'O'
                boards[opponent][row][col] = 'O'

            # Check if the game is over
            all_ships_sunk = all(data["hits"] == data["size"] for data in ship_data[opponent].values())
            if all_ships_sunk:
                print(f"\nGame Over! {players[active_player]} wins!")
                print("\nFinal Boards:")
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
    #Main function to start and manage the game.
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

    #Setup ships for both the players
    setup_ships(player1, board1, ships)
    setup_ships(player2, board2, ships)

    start = input("\nReady to start the game? (Y/N): ").upper()
    if start == 'Y':
        play_game(player1, player2, board1, board2, ships)
    else:
        print("GAME OVER. Hope you had a good time!")


if __name__ == "__main__":
    main()
