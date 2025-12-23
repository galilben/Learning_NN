import tensorflow
from GameFunctions import *
from tensorflow import keras
import numpy as np
from training import *
from model import *

#create a data set of games-> save all winning games only to calculate in network best winning not drawing moves
def Get_db():
    X = []
    Y = []

    for _ in range(20000):
        states, moves, winner = train_with_random_game()
        if winner == 2:
            for s, m in zip(states, moves):
                X.append(s)
                target = np.zeros(9)
                target[m] = 1
                Y.append(target)
    X = tensorflow.convert_to_tensor(X, dtype=tensorflow.float32)
    Y = tensorflow.convert_to_tensor(Y, dtype=tensorflow.float32)
    return X,Y


#call model to get a result


def play(model):
    global board

    print("Hello to u player\nhere is my tictactoe random game \nsay bye if you are done")
    player_choise=""
    board=np.zeros(9)
    moves=[]
    while player_choise!="bye":
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
                    moves.append((board,choise,1))
                    if(check_winner(board)!=0):
                        print(f"You win!!")
                        model.adjust_loss(moves,1) #real time learn from games
                        moves=[]
                        board=np.zeros(9)
                    elif(np.all(board!=0)):
                        print("its a draw")
                        board=np.zeros(9)
                    else:
                        ai = model.ai_move(board)
                        board[ai] = -1
                        moves.append((board,ai,-1))
                        print("AI played:", ai)
                        if(check_winner(board)!=0):
                            print(f"You lose!!")
                            board=np.zeros(9)
                            model.adjust_model(moves,-1) #real time learn from games
                            moves=[]
            else:
                print("choises 0->9 or bye")


model=model_tic_tac_toe()
training(model=model)
play(model)

