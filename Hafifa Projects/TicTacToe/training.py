from GameFunctions import *
import tensorflow

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
    return 0,0,0    #in case of draw doesnt matter


def self_play(model):
    board = np.zeros(9)
    memory = []
    player = 1

    for _ in range(9):
        state = board*-1
        probs = model.model(tensorflow.expand_dims(state, 0))[0].numpy() 
        probs[board != 0] = 0
        probs /= probs.sum()
        action = np.random.choice(9, p=probs)
        memory.append((state, action, player))
        board[action] = player
        winner = check_winner(board)
        if winner != 0 or np.all(board != 0):
            return memory, winner

        player = player*-1
    return 0,0

def training(model):
    for i in range(5000):
        print(i)
        memory,winner=self_play(model)
        if winner!=0:
            model.adjust_model(memory,winner)

