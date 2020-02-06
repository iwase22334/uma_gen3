#!/usr/bin/env python3
import UmaDatasetGen3

import numpy as np
import os
import sys

# Gathering data from database
def provision(fromymd, toymd, name):
    uma_data = UmaDatasetGen3.UmaDatasetGen3()

    x_train, y_train = uma_data.load_data(fromymd, toymd)

    np.save('x_' + name, x_train, True, False)
    np.save('y_' + name, y_train, True, False)

    print('x_train', len(x_train) )
    print('x_train[]', [len(x_train[i]) for i in range(len(x_train))] )
    print('x_train[0][0]', len(x_train[0][0]))
    print('x_train[1][0]', len(x_train[1][0]))

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("usage: generate_fragment.py fromymd toymd name")

    fromymd = sys.argv[1]
    toymd = sys.argv[2]
    name = sys.argv[3]

    print("name: ", name)
    print("everydb: ", os.environ.get('DB_EVERYDB2'))
    print("uma_processed: ", os.environ.get('DB_UMA_PROCESSED'))
    print(fromymd, "~", toymd)

    provision(fromymd, toymd, name)

    print("complete")

