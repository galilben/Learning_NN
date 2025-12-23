import tensorflow
from tensorflow import keras
import numpy as np
from GameFunctions import *
class model_tic_tac_toe:
    def __init__(self):
        self.loss_fn=keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        self.optimizer=keras.optimizers.Adam()
        self.model = keras.Sequential([
            keras.layers.Input(shape=(9,)), 
            keras.layers.Dense(64, activation='relu'), 
            keras.layers.Dense(64, activation='relu'), 
            keras.layers.Dense(9, activation='softmax')
        ])
        
        self.model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
    
    
    def grad(self,model, inputs,result):
        with tensorflow.GradientTape() as tape:
            loss = 0
            for state, action, player in inputs:
                if(player==result):
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
        probs[board != 0] = 0
        if probs.sum() == 0:
            return random_move(board)

        return np.argmax(probs)

    
    