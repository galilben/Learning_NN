import numpy as np
global wins
global board
wins=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
base_state=[0,0,0,0,0,0,0,0,0]
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
    board=np.array(base_state)
    print("new game starting")
def check_winner(state):
    global wins
    for w in wins:
        if state[w[1]]==state[w[0]]==state[w[2]] and state[w[0]]!=0:
            return state[w[0]]
    return 0
def random_move(state):
    options=np.where(state==0)[0]
    return np.random.choice(options)

print("Hello to u player\nhere is my tictactoe random game \nsay bye if you are done")
player_choise=""
new_game=True
board=np.array(base_state)

while player_choise!="bye":
    if new_game:
        random_bit = np.random.choice([0, 1])
        print(random_bit)
        if random_bit==1:
            board[random_move(board)]=2
        new_game=False
    print_board(board)
    player_choise=input("your choise ->")
    if(not is_number(player_choise)):
        print("insert number or bye")
    else:
        choise=int(player_choise)
        if(choise>=0 and choise<=8):
            if board[choise]!=0:
                print("illigle choise :(")
            else:
                board[choise]=1
                if(check_winner(board)!=0):
                    print(f"You win!!")
                    reset_game()
                    new_game=True

                else:
                    board[random_move(board)]=2
                    if(check_winner(board)!=0):
                        print(f"You lose!!")
                        reset_game()
                        new_game=True

        else:
            print("choises 0->9 or bye")

