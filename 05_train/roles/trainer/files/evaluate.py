#!/usr/bin/env python3

import format_data

import numpy as np
import os
import sys
import keras
from keras.models import Model
from keras import regularizers
from keras.layers import Input, Dense, Concatenate
from keras.optimizers import RMSprop


def evaluate(modelname, x_eval, y_eval):
    print(modelname)
    model = keras.models.load_model(modelname, compile=True)

    score = model.evaluate(x_eval, y_eval, verbose=1)

    race_list, *uma_list = x_eval

    sum_syusso = 0.0
    for race in race_list:
        sum_syusso = sum_syusso + race[1]
    average = sum_syusso / len(race_list)
    return score[0], score[1], average, len(race_list)

if __name__ == "__main__":
    args = sys.argv
    if not len(args) == 2:
        print('Usage: evaluate.py <model.h5>')
        exit()

    modelname = args[1]
    loss, accuracy, average, racenum = evaluate(modelname)
    print('Test loss:', loss)
    print('Test accuracy:', accuracy)
    print('Test race num: ', racenum)
    print('Average of syusso tosu:', average)
    print('Expected accuracy:', 1./average)

