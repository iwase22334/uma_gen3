#!/usr/bin/env python3
import evaluate
import format_data

import numpy as np
import itertools
import os
import sys 
import pickle
import keras
from keras.models import Model
from keras import regularizers
from keras.layers import Input, Dense, Concatenate, Dropout
from keras.optimizers import RMSprop

def generate_modelname(param):
    name, ext = os.path.splitext(os.path.basename(__file__))
    filename = name;
    for p in param: filename = filename + '_' + str(p)
    return filename

def train(neckdim, uma_depth, merged_depth, regularize_const, dropout_rate):
    print(neckdim, uma_depth, merged_depth, regularize_const, dropout_rate)

    ## Define network 
    race_info_dim = 33
    uma_info_dim  = 393
    max_syusso    = 18

    ## Layer for Uma info
    input_uma = list()
    for i in range(max_syusso):
        input_uma.append(Input(shape=(race_info_dim + uma_info_dim,)))

    ## input layer
    uma_dense_1 = Dense(race_info_dim + uma_info_dim, kernel_regularizer=regularizers.l2(regularize_const), activation='tanh')
    hidden_uma_branch_1 = [ list() for i in range(max_syusso) ]
    for i in range(max_syusso):
        hidden_uma_branch_1[i].append(uma_dense_1(input_uma[i]))

    ## hidden layer
    for i in range(uma_depth - 1):
        for branch_no in range(max_syusso):
            branch = hidden_uma_branch_1[branch_no]
            tail = branch[len(branch) - 1]
            branch.append(uma_dense_1(tail))

            tail = branch[len(branch) - 1]
            branch.append(Dropout(dropout_rate)(tail))

    ## Layer for concatenamting race info and uma info
    hidden_m = Concatenate()([branch[len(branch) - 1] for branch in hidden_uma_branch_1])

    hidden_con = list()
    hidden_con.append(Dense(neckdim, kernel_regularizer=regularizers.l2(0.001), activation='tanh')(hidden_m))
    for i in range(merged_depth - 1):
        tail = hidden_con[len(hidden_con) - 1]
        hidden_con.append(Dense(neckdim, kernel_regularizer=regularizers.l2(0.001), activation='tanh')(tail))

    tail = hidden_con[len(hidden_con) - 1]
    predictions = Dense(18, activation='softmax')(tail)

    model = Model(inputs=input_uma, outputs=predictions)

    ## Cmpile network
    model.compile(optimizer=RMSprop(), loss='categorical_crossentropy', metrics=['accuracy'])

    ## train
    early_stopping = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.0001, patience=5, verbose=0, mode='auto') 
    model.fit(x_train, y_train, epochs=256, verbose=1, batch_size=2048, callbacks=[early_stopping])

    ## save
    modelname = generate_modelname([neckdim, uma_depth, merged_depth, regularize_const, dropout_rate])
    model.save(modelname + '.h5')

    with open(modelname + '.hist', 'wb') as file_pi:
        pickle.dump(model.history, file_pi)

def load_traindata():
    project_path = os.environ.get('UMA_PROJECT_PATH')

    ## Gathering data from database
    print('loading x_train')
    tmp_list = np.load(file = project_path + '/x_train.npy', allow_pickle=True)
    print('load complete  ')
    x_train = format_data.format_data(tmp_list)

    print(len(x_train))
    print(len(x_train[0]))
    print(len(x_train[0][0]))

    print('loading y_train')
    y_train = np.load(file = project_path + '/y_train.npy', allow_pickle=True)

    return x_train, y_train

def load_evaldata():
    print('loading x_eval')

    project_path = os.environ.get('UMA_PROJECT_PATH')

    tmp_list = np.load(file = project_path + '/x_eval.npy', allow_pickle=True)
    x_eval = format_data.format_data(tmp_list)

    print('loading y_eval')
    y_eval = np.load(file = project_path + '/y_eval.npy', allow_pickle=True)

    return x_eval, y_eval

if __name__ == "__main__":

    if not len(sys.argv) == 1:
        print('Usage: trainer.py')
        exit()

    x_train, y_train = load_traindata()
    x_eval, y_eval = load_evaldata()

    # set parameter 
    dropout_rate_list       = [0.0, 0.3]
    neck_dimension_list     = [18, 54]
    uma_depth_list          = [1 ]
    merged_depth_list       = [1, 2]
    regularize_const_list   = [0.001, 0.0003]

    param = list()
    for nd in neck_dimension_list:
        for do in dropout_rate_list:
            for md in merged_depth_list:
                for ud in uma_depth_list:
                    for rcd in regularize_const_list:
                        param.append([nd, ud, md, rcd, do])

    print(param)
    count = 0
    for neckdim, uma_depth, merged_depth, regularize_const, dropout_rate in param:
        count = count + 1
        modelname = generate_modelname([neckdim, uma_depth, merged_depth, regularize_const, dropout_rate])
        print(modelname)

        if os.path.exists(modelname + '.h5'):
            continue

        print('===========================')
        print('[%d / %d]' % (count, len(param)))
        print('===========================')
        train(neckdim, uma_depth, merged_depth, regularize_const, dropout_rate)
        loss, accuracy, average, racenum = evaluate.evaluate(generate_modelname([neckdim, uma_depth, merged_depth, regularize_const, dropout_rate]) + '.h5', 
                                                            x_eval, y_eval)

        print('Test loss:', loss)
        print('Average of syusso tosu:', average)
        print('Test     accuracy:', accuracy)
        print('Expected accuracy:', 1./average)

        with open('log_trainer.txt', 'a') as f:
            print(modelname + ':' + str(accuracy), file=f)


