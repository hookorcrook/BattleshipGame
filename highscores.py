def save_high_score(file_name, player_name, turns):
    """
    Saves the high score to a file.
    Params:
        file_name: Name of the file to save scores.
        player_name: Name of the player.
        turns: Number of turns taken by the player to win.
    """
    with open(file_name, 'a') as file:
        file.write(f"{player_name},{turns}\n")


def get_high_score(file_name):
    """
    Reads the high score from a file.
    Params:
        file_name: Name of the file to read scores.
    """
    ##Returns a tuple with player_name and turns of the highest score lowest turns.
    try:
        with open(file_name, 'r') as file:
            scores = [line.strip().split(',') for line in file.readlines()]
            scores = [(name, int(turns)) for name, turns in scores]
            return min(scores, key=lambda x: x[1])  # Player with minimum turns
    except FileNotFoundError:
        return None  # No high score file found
    except ValueError:
        return None  # Invalid data in file
