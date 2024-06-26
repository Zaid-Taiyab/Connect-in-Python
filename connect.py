import os
import time

ROWS = 6
COLUMNS = 7

def initialize_grid():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_grid(grid):
    print()
    for row in grid:
        print('| ' + ' | '.join(row) + ' |')
    print('-' * (4 * COLUMNS + 1))

def get_token_number():
    while True:
        try:
            tokens = int(input("Enter the number of tokens to connect (3, 4, or 5): "))
            if tokens in [3, 4, 5]:
                return tokens
            else:
                print("Please enter 3, 4, or 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def make_move(grid, column, player):
    for row in range(ROWS-1, -1, -1):
        if grid[row][column] == ' ':
            grid[row][column] = player
            return True
    return False

def check_vertical_win(grid, player, tokens_to_win):
    for col in range(COLUMNS):
        for row in range(ROWS - tokens_to_win + 1):
            if all(grid[row + i][col] == player for i in range(tokens_to_win)):
                return True
    return False

def check_horizontal_win(grid, player, tokens_to_win):
    for row in range(ROWS):
        for col in range(COLUMNS - tokens_to_win + 1):
            if all(grid[row][col + i] == player for i in range(tokens_to_win)):
                return True
    return False

def check_diagonal_win(grid, player, tokens_to_win):
    # Check \-diagonals
    for row in range(ROWS - tokens_to_win + 1):
        for col in range(COLUMNS - tokens_to_win + 1):
            if all(grid[row + i][col + i] == player for i in range(tokens_to_win)):
                return True

    # Check /-diagonals
    for row in range(ROWS - tokens_to_win + 1):
        for col in range(tokens_to_win - 1, COLUMNS):
            if all(grid[row + i][col - i] == player for i in range(tokens_to_win)):
                return True

    return False

def replay_game(move_history):
    replay_grid = initialize_grid()

    for move in move_history:
        column, player = move
        make_move(replay_grid, column, player)
        print_grid(replay_grid)
        time.sleep(1)  # Pause for 1 second between moves

def main():
    play_again = 'Y'

    while play_again.upper() == 'Y':
        tokens_to_win = get_token_number()
        grid = initialize_grid()
        print_grid(grid)

        current_player = 'R'
        total_moves = 0
        move_history = []

        while total_moves < ROWS * COLUMNS:
            try:
                column = int(input(f"Player {current_player}, pick a column (1-{COLUMNS}): ")) - 1

                if 0 <= column < COLUMNS:
                    if make_move(grid, column, current_player):
                        print_grid(grid)
                        move_history.append((column, current_player))

                        if (check_vertical_win(grid, current_player, tokens_to_win) or
                                check_horizontal_win(grid, current_player, tokens_to_win) or
                                check_diagonal_win(grid, current_player, tokens_to_win)):
                            print(f"Player {current_player} wins!")
                            break

                        total_moves += 1
                        current_player = 'Y' if current_player == 'R' else 'R'
                    else:
                        print("Column is full. Please pick another column.")
                else:
                    print(f"Invalid column. Please enter a number between 1 and {COLUMNS}.")

            except ValueError:
                print("Invalid input. Please enter a number.")

        if total_moves == ROWS * COLUMNS:
            print("It's a draw!")

        # Replay option
        replay_choice = input("Game over. Press 'Q' to quit, 'R' to replay, or any other key to continue: ").upper()
        if replay_choice == 'R':
            replay_game(move_history)

        play_again = input("Do you want to play again? (Y/N): ").upper()

    print("Goodbye!")

if __name__ == "__main__":
    main()
