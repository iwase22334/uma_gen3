import numpy as np

def format_data(raw_data):
    formated_data = list()
    race_list, *uma_list= raw_data

    print(len(race_list[0]))
    print(len(uma_list[0][0]))

    for uma in uma_list:
        ru_list = list()

        for r, u in zip(race_list, uma):
            ru_list.append(np.append(r, u))

        formated_data.append(ru_list)
    return formated_data

