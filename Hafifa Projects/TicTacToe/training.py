from GameFunctions import *
def random_move(state):
    options=np.where(state==0)[0]
    return np.random.choice(options)


def train_with_random_game():
    board = np.zeros(9)
    boards_seen = []
    moves = []
    player=1
    for i in range(9):
        move = random_move(board)
        boards_seen.append(board.copy())
        moves.append(move)
        board[move] = player
        if check_winner(board):
            return boards_seen, moves, player
        player =player^1^2
    return 0,0,0 #in case of draw doesnt matter

