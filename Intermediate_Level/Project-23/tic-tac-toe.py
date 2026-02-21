import math

# Initialize board
board = [' ' for _ in range(9)]

# Print the board
def print_board():
    for i in range(3):
        print(board[i*3], '|', board[i*3+1], '|', board[i*3+2])
        if i < 2:
            print('--+---+--')

# Check for winner
def check_winner():
    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # columns
        [0,4,8],[2,4,6]           # diagonals
    ]
    for condition in win_conditions:
        a, b, c = condition
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Draw'
    return None

# Minimax algorithm
def minimax(is_maximizing):
    result = check_winner()
    if result == 'X':
        return -1
    elif result == 'O':
        return 1
    elif result == 'Draw':
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# Find best move for AI
def best_move():
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

# Main game loop
def play_game():
    print("You are X, AI is O")
    print_board()

    while True:
        # Player move
        player_move = int(input("Enter position (0-8): "))
        if board[player_move] == ' ':
            board[player_move] = 'X'
        else:
            print("Invalid move!")
            continue

        if check_winner():
            break

        # AI move
        ai_move = best_move()
        board[ai_move] = 'O'

        print_board()

        if check_winner():
            break

    result = check_winner()
    print_board()
    print("Result:", result)

play_game()