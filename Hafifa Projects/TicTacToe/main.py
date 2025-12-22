import tensorflow
from GameFunctions import *
from tensorflow import keras
import numpy as np

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
def ai_move(board):
    board = board.astype(np.float32)
    probs = model(tensorflow.expand_dims(board, axis=0))[0].numpy()

    # mask illegal moves
    probs[board != 0] = 0

    if probs.sum() == 0:
        return random_move(board)

    return np.argmax(probs)

#basic loss function?
loss_fn=keras.losses.SparseCategoricalCrossentropy(from_logits=True)

#passing with 2 hiddens? 64 8*8 which is the number of max options squered
model = keras.Sequential([
    keras.layers.Input(shape=(9,)),  #9 inputs -> 1 for each space
    keras.layers.Dense(64, activation='relu'), #64 hidden layers-> 
    keras.layers.Dense(64, activation='relu'), #second hidden layer
    keras.layers.Dense(9, activation='softmax') # 9 output options to show the odds of each move
])





model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

#model.fit -> give data to model and train it on that data
X,Y=Get_db()
model.fit(X, Y, epochs=25, batch_size=32)



def play():
    global board

    print("Hello to u player\nhere is my tictactoe random game \nsay bye if you are done")
    player_choise=""
    board=np.zeros(9)
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
                    if(check_winner(board)!=0):
                        print(f"You win!!")
                        board=np.zeros(9)
                    elif(np.all(board!=0)):
                        print("its a draw")
                        board=np.zeros(9)
                    else:
                        ai = ai_move(board)
                        board[ai] = 2
                        print("AI played:", ai)
                        if(check_winner(board)!=0):
                            print(f"You lose!!")
                            board=np.zeros(9)
            else:
                print("choises 0->9 or bye")
play()

