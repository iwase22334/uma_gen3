#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd

def to_list_in_list(array_in_list):
    return [ arr.tolist() for arr in array_in_list ]

def load():
    project_path = os.environ.get('UMA_PROJECT_PATH')
    raw_data = np.load(file = project_path + '/x_train.npy', allow_pickle=True)
    return raw_data

def load_pd():
    project_path = os.environ.get('UMA_PROJECT_PATH')
    raw_data = np.load(file = project_path + '/x_train.npy', allow_pickle=True)

    # ignore race_info
    uma_dfl = [ pd.DataFrame(to_list_in_list(u)) for u in raw_data ]

    return uma_dfl

def format_data(raw_data):
    formated_data = list()

    # ignore race_info
    race_list, *uma_list = raw_data

    uma_dfl = [ pd.DataFrame(to_list_in_list(u)) for u in uma_list ]

    for uma in uma_dfl:
        ru_list = list()

        basic = uma.iloc[:,10:19]
        rating_shiba = uma.iloc[:,21] + uma.iloc[:,22]
        rating_dirt  = uma.iloc[:,23] + uma.iloc[:,24]

        uma_selected = pd.concat([basic, rating_shiba, rating_dirt], axis=1)

        for u in uma_selected.values:
            ru_list.append(np.array(u))

        formated_data.append(ru_list)

    return formated_data

if __name__ == '__main__':
    raw = load()
    fdata = format_data(raw)
    print(len(fdata))
    print(len(fdata[0]))
    print(len(fdata[1][0]))
    print(fdata[1][0])
    print(fdata[1][1])
