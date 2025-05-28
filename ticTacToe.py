import random


def smart_ai(grid, ai_player, human_player):
    # get a list of all valid moves
    moves = valid_moves(grid)

    # check if AI can win
    for move in moves:
        hypothetical_grid = play(grid, move, ai_player)  # simulate the AI making the move
        if check_win(hypothetical_grid, ai_player):
            return move  # return the winning move

    # else, block the player's winning move
    for move in moves:
        hypothetical_grid = play(grid, move, human_player)  # simulate the player making the move
        if check_win(hypothetical_grid, human_player):
            return move  # return the move to block the player

    # else, if center is available, pick it (optimal for first move)
    if grid[4] == '-':
        return 4

    # pick a random valid move
    return random.choice(moves)


def minimax(grid, depth, is_maximizing, ai_player, human_player):
    # base cases
    if check_win(grid, ai_player):  # AI wins
        return 1
    if check_win(grid, human_player):  # user wins
        return -1
    if '-' not in grid:  # tie / draw
        return 0

    # recursion
    if is_maximizing:
        best_score = float('-inf')  # AI trying to maximize
        for move in valid_moves(grid):
            hypothetical_grid = play(grid, move, ai_player)
            score = minimax(hypothetical_grid, depth + 1, False, ai_player, human_player)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')  # user trying to minimize
        for move in valid_moves(grid):
            hypothetical_grid = play(grid, move, human_player)
            score = minimax(hypothetical_grid, depth + 1, True, ai_player, human_player)
            best_score = min(best_score, score)
        return best_score


def minimax_ai(grid, ai_player, human_player):
    best_score = float('-inf')
    best_move = None

    for move in valid_moves(grid):
        hypothetical_grid = play(grid, move, ai_player)  # sim AI move
        score = minimax(hypothetical_grid, 0, False, ai_player, human_player)  # evaluate with minimax
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def play(grid, position, player):
    # strings are immutable, have to generate a new string
    if grid[position] == '-':
        grid = grid[:position] + player + grid[position + 1:]
    return grid


def valid_moves(grid):
    # check if it contains a "-", then it is valid
    valid = []
    for i, position in enumerate(grid):
        if position == "-":
            valid.append(i)
    return valid


def check_win(grid, player):
    # player will contain either X or O
    # grid is a 9 character string

    # player wins if there are 3 of the player in a row
    win = player + player + player

    # horizontal wins
    if grid[:3] == win or grid[3:6] == win or grid[6:] == win:
        return True

    # vertical wins
    if grid[0] + grid[3] + grid[6] == win or grid[1] + grid[4] + grid[7] == win or grid[2] + grid[5] + grid[8] == win:
        return True

    # diagonal wins
    if grid[0] + grid[4] + grid[8] == win or grid[2] + grid[4] + grid[6] == win:
        return True

    # else, no wins so it is false
    return False

def visualize_grid(grid):
    for i in range(0, 9, 3):  # loop through the grid in steps of 3
        print(grid[i], "|", grid[i+1], "|", grid[i+2])
    print()



def get_player_move(grid):
    while True:
        try:
            # ask the player to enter a move
            move = input("Your turn: ").strip()
            row, col = map(int, move.split())  # split input into row and column
            index = row * 3 + col  # convert 2dimensional row/col into 1dimensional index

            # validate the move
            if grid[index] == '-':
                return index  # valid move, return the index
            else:
                print("This position is already taken. try again.")
        except (ValueError, IndexError):
            print("Invalid input. please enter row and column as numbers between 0 and 2, like '0 0' ")


def main():
    # initialize the grid
    grid = '---------'  # 9-character string representing the grid
    current_player = 'X'  # start with the human player
    ai_player = 'O'  # ai is o
    human_player = 'X'  # human is x

    # randomise current_player
    #random_player = []
    #random_player.append(ai_player)
    #random_player.append(human_player)
    # current_player = random.choice(random_player)

    print("Welcome to tic tac toe!")
    print("You are 'X' and the AI is 'O'.\n")
    print("00 | 01 | 02\n")
    print("10 | 11 | 12\n")
    print("20 | 21 | 22\n")
    print("Enter your move (row (horizontal) and column (vertical), like '1 1' for the middle): ")

    while True:
        visualize_grid(grid) #display the grid

        if check_win(grid, human_player): #if player won
            print("You win!")
            break
        elif check_win(grid, ai_player): #if AI won
            print("AI wins! :)")
            break
        elif '-' not in grid: #if grid full
            print("It's a tie!")
            break

        # handle current player turn
        if current_player == human_player:
            #print("Your turn:")
            move = get_player_move(grid)
            grid = play(grid, move, human_player)
        else:
            print("AI's turn:")
            move = minimax_ai(grid, ai_player, human_player)
            grid = play(grid, move, ai_player)

        # switch to the next player
        if current_player == human_player:
            current_player = ai_player
        else:
            current_player = human_player


if __name__ == "__main__":
    main()