#!/usr/bin/env python3
import os
import numpy as np
import psycopg2
from psycopg2  import extras
import pandas as pd
from tqdm import tqdm
table_name = 'uma_gen3_train'

create_table_query = ('''
CREATE TABLE %s (
 id char(8),
 idsub char(2),
 umaban real,
 sexoh1 real,
 sexoh2 real,
 sexoh3 real,
 tozaioh1 real,
 tozaioh2 real,
 futan real,
 bataijyu real,
 zogensa real,
 zogensa_negative real,
 liveyear real,
 srating1 real,
 srating_diff1 real,
 selapsed_year1 real,
 srating2 real,
 srating_diff2 real,
 selapsed_year2 real,
 srating3 real,
 srating_diff3 real,
 selapsed_year3 real,
 drating1 real,
 drating_diff1 real,
 delapsed_year1 real,
 drating2 real,
 drating_diff2 real,
 delapsed_year2 real,
 drating3 real,
 drating_diff3 real,
 delapsed_year3 real,
 ruikeishiba real,
 ruikeidirt real,
 ruikeichakukaisu real,
 chaku real,
 kyaku real,
 u12sh real,
 u14sh real,
 u16sh real,
 u18sh real,
 u20sh real,
 u22sh real,
 u24sh real,
 u28sh real,
 o28sh real,
 u12di real,
 u14di real,
 u16di real,
 u18di real,
 u20di real,
 u22di real,
 u24di real,
 u28di real,
 o28di real,
 chaku_r1  real,
 chaku_r2  real,
 chaku_r3  real,
 chaku_r4  real,
 chaku_r5  real,
 chaku_r6  real,
 kyaku_r1 real,
 kyaku_r2 real,
 kyaku_r3 real,
 kyaku_r4 real,
 u12sh_r1 real,
 u12sh_r2 real,
 u12sh_r3 real,
 u12sh_r4 real,
 u12sh_r5 real,
 u12sh_r6 real,
 u14sh_r1 real,
 u14sh_r2 real,
 u14sh_r3 real,
 u14sh_r4 real,
 u14sh_r5 real,
 u14sh_r6 real,
 u16sh_r1 real,
 u16sh_r2 real,
 u16sh_r3 real,
 u16sh_r4 real,
 u16sh_r5 real,
 u16sh_r6 real,
 u18sh_r1 real,
 u18sh_r2 real,
 u18sh_r3 real,
 u18sh_r4 real,
 u18sh_r5 real,
 u18sh_r6 real,
 u20sh_r1 real,
 u20sh_r2 real,
 u20sh_r3 real,
 u20sh_r4 real,
 u20sh_r5 real,
 u20sh_r6 real,
 u22sh_r1 real,
 u22sh_r2 real,
 u22sh_r3 real,
 u22sh_r4 real,
 u22sh_r5 real,
 u22sh_r6 real,
 u24sh_r1 real,
 u24sh_r2 real,
 u24sh_r3 real,
 u24sh_r4 real,
 u24sh_r5 real,
 u24sh_r6 real,
 u28sh_r1 real,
 u28sh_r2 real,
 u28sh_r3 real,
 u28sh_r4 real,
 u28sh_r5 real,
 u28sh_r6 real,
 o28sh_r1 real,
 o28sh_r2 real,
 o28sh_r3 real,
 o28sh_r4 real,
 o28sh_r5 real,
 o28sh_r6 real,
 u12di_r1 real,
 u12di_r2 real,
 u12di_r3 real,
 u12di_r4 real,
 u12di_r5 real,
 u12di_r6 real,
 u14di_r1 real,
 u14di_r2 real,
 u14di_r3 real,
 u14di_r4 real,
 u14di_r5 real,
 u14di_r6 real,
 u16di_r1 real,
 u16di_r2 real,
 u16di_r3 real,
 u16di_r4 real,
 u16di_r5 real,
 u16di_r6 real,
 u18di_r1 real,
 u18di_r2 real,
 u18di_r3 real,
 u18di_r4 real,
 u18di_r5 real,
 u18di_r6 real,
 u20di_r1 real,
 u20di_r2 real,
 u20di_r3 real,
 u20di_r4 real,
 u20di_r5 real,
 u20di_r6 real,
 u22di_r1 real,
 u22di_r2 real,
 u22di_r3 real,
 u22di_r4 real,
 u22di_r5 real,
 u22di_r6 real,
 u24di_r1 real,
 u24di_r2 real,
 u24di_r3 real,
 u24di_r4 real,
 u24di_r5 real,
 u24di_r6 real,
 u28di_r1 real,
 u28di_r2 real,
 u28di_r3 real,
 u28di_r4 real,
 u28di_r5 real,
 u28di_r6 real,
 o28di_r1 real,
 o28di_r2 real,
 o28di_r3 real,
 o28di_r4 real,
 o28di_r5 real,
 o28di_r6 real,
 p1umaban real,
 p1sexoh1 real,
 p1sexoh2 real,
 p1sexoh3 real,
 p1tozaioh1 real,
 p1tozaioh2 real,
 p1futan real,
 p1bataijyu real,
 p1zogensa real,
 p1zogensa_negative real,
 p1kakuteijyuni real,
 p1syokin real,
 p1time real,
 p1timediff real,
 p1vel real,
 p1harontimel3 real,
 p1haronvel real,
 p1kyakusitukubun1 real,
 p1kyakusitukubun2 real,
 p1kyakusitukubun3 real,
 p1kyakusitukubun4 real,
 p1pastdays real,
 p2umaban real,
 p2sexoh1 real,
 p2sexoh2 real,
 p2sexoh3 real,
 p2tozaioh1 real,
 p2tozaioh2 real,
 p2futan real,
 p2bataijyu real,
 p2zogensa real,
 p2zogensa_negative real,
 p2kakuteijyuni real,
 p2syokin real,
 p2time real,
 p2timediff real,
 p2vel real,
 p2harontimel3 real,
 p2haronvel real,
 p2kyakusitukubun1 real,
 p2kyakusitukubun2 real,
 p2kyakusitukubun3 real,
 p2kyakusitukubun4 real,
 p2pastdays real,
 p3umaban real,
 p3sexoh1 real,
 p3sexoh2 real,
 p3sexoh3 real,
 p3tozaioh1 real,
 p3tozaioh2 real,
 p3futan real,
 p3bataijyu real,
 p3zogensa real,
 p3zogensa_negative real,
 p3kakuteijyuni real,
 p3syokin real,
 p3time real,
 p3timediff real,
 p3vel real,
 p3harontimel3 real,
 p3haronvel real,
 p3kyakusitukubun1 real,
 p3kyakusitukubun2 real,
 p3kyakusitukubun3 real,
 p3kyakusitukubun4 real,
 p3pastdays real,
 valid real,
 PRIMARY KEY (id, idsub)
);
''' % table_name ).replace('\n', '')

def create_table(uma_processed):

    try:
        with uma_processed.cursor() as processed_cur:
            processed_cur.execute("select exists(select * from information_schema.tables where table_name=%s)"
                        , (table_name,))

            if not processed_cur.fetchone()[0]:
                processed_cur.execute(create_table_query)
                uma_processed.commit()
                print('table added')

            else:
                print('table exist')

    except Exception as e:
        print(e)

def insert(con_processed, data):
    with con_processed.cursor() as processed_cur:
        query = "INSERT INTO %s " % table_name+ "VALUES %s"
        print(query)
        extras.execute_values(processed_cur, query, data)

    con_processed.commit()

#def insert(con_processed, data):
#    with con_processed.cursor() as processed_cur:
#        query = "INSERT INTO %s " % table_name+ "VALUES ( \'%s\', \'%s\'" % (data[0][0], data[0][1])
#
#        for d in data[0][2:]:
#            query = query + ", %s" % d
#
#        query = query + ")"
#
#        print(query)
#        processed_cur.execute(query)
#
#    con_processed.commit()


def to_list_in_list(array_in_list):
    return [ arr.tolist() for arr in array_in_list ]

def load():
    project_path = os.environ.get('UMA_PROJECT_PATH')
    raw_data = np.load(file = project_path + '/x_train.npy', allow_pickle=True)
    return raw_data

if __name__ == '__main__':
    try:
        con_processed = psycopg2.connect(os.environ.get('DB_UMA_PROCESSED'))
    except Exception as e:
        print('psycopg2: connecting uma_processed faied')
        raise e

    create_table(con_processed)

    print('loading data')
    race, *uma_list = load();

    for uma, i in zip(uma_list, range(18)):
        datalist = []

        for u, j in tqdm(zip(uma, range(len(uma)))):
            datalist.append((str(j+1).rjust(8, '0'), str(i+1).rjust(2, '0')) 
                            + tuple('{:.6g}'.format(round(elem, 6)) for elem in u))

        print(datalist[0:1])
        print(len(datalist[0]))
        print(type(datalist[0]))

        insert(con_processed, datalist)

    con_processed.close()




