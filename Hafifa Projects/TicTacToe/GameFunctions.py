import numpy as np
global board
global wins 
wins=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
board=np.zeros(9)

def print_board(state):
    print(f"|{state[0]}||{state[1]}||{state[2]}|")
    print(f"|{state[3]}||{state[4]}||{state[5]}|")
    print(f"|{state[6]}||{state[7]}||{state[8]}|")


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        try:
            return False
        except ValueError:
            return False
        

def reset_game():
    global board
    print_board(board)
    board=np.zeros(9)
    print("new game starting")


def check_winner(state):
    for w in wins:
        if state[w[1]]==state[w[0]]==state[w[2]] and state[w[0]]!=0:
            return state[w[0]]
    return 0

def random_move(state):
    options=np.where(state==0)[0]
    return np.random.choice(options)

