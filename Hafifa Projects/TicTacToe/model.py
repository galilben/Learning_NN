import tensorflow
from tensorflow import keras
import numpy as np
from GameFunctions import *
class model_tic_tac_toe:
    def __init__(self):
        #basic loss function?
        self.loss_fn=keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        self.optimizer=keras.optimizers.Adam()
        #passing with 2 hiddens? 64 8*8 which is the number of max options squered
        self.model = keras.Sequential([
            keras.layers.Input(shape=(9,)),  #9 inputs -> 1 for each space
            keras.layers.Dense(64, activation='relu'), #64 hidden layers-> 
            keras.layers.Dense(64, activation='relu'), #second hidden layer
            keras.layers.Dense(9, activation='softmax') # 9 output options to show the odds of each move
        ])
        
        self.model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
    
    
    def grad(self,model, inputs,result):
        with tensorflow.GradientTape() as tape:
            loss = 0
            for state, action, player in inputs:
                reward = result * player
                probs = model(tensorflow.expand_dims(state, 0))
                log_prob = tensorflow.math.log(probs[0, action] + 1e-8)
                loss += -reward * log_prob
            return tape.gradient(loss, model.trainable_variables)
    
    def adjust_model(self,memory,winner):
        grads = self.grad(self.model, memory,winner)
        self.optimizer.apply_gradients(zip(grads,self.model.trainable_variables))

    def ai_move(self,board):
        board = board.astype(np.float32)
        probs = self.model(tensorflow.expand_dims(board, axis=0))[0].numpy()

        # mask illegal moves
        probs[board != 0] = 0

        if probs.sum() == 0:
            return random_move(board)

        return np.argmax(probs)

    
    