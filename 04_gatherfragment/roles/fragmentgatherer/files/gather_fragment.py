#!/usr/bin/env python3
import numpy as np
import os
import sys
import pickle

## Gathering data from database
if __name__ == "__main__":
    args = sys.argv

    if len(args) != 3:
        print("usage: gather_fragment.py <dataname> <divnum>")
        exit()

    dataname = args[1]
    divnum = int(args[2])

    x = [ list() for i in range(19) ]

    for i in range(divnum):
        print('no: %d' % i)
        no = i + 1

        x_file_name = 'x_%s_%02d.npy' % (dataname, no)
        fragment = np.load(file=x_file_name, allow_pickle=True)
        for felem, telem in zip(fragment, x):
            for f in felem:
                telem.append(f)

        print(x_file_name)

    print('saving x_%s' % dataname)
    try:
        np.save('x_%s.npy' % dataname , x, True, False)
    except:
        print(sys.exc_info())
        exit(-1)

    print('x')
    print('len x', len(x))
    print('len x[]', [len(x[i]) for i in range(len(x))] )
    print('len x[0][0]', len(x[0][0]))
    print('len x[1][0]', len(x[1][0]))

    del x

    y = list()
    for i in range(divnum):
        print('no: %d' % i)
        no = i + 1

        y_file_name = 'y_%s_%02d.npy' % (dataname, no)
        for elem in np.load(file=y_file_name, allow_pickle=True):
            y.append(elem)

        print(y_file_name)

    print('saving y')
    try:
        np.save('y_%s.npy' % dataname, y, True, False)
    except:
        print(sys.exc_info())
        exit(-1)

    print('y')
    print('len y', len(y))
    print('len y[0]', len(y[0]))

    del y

