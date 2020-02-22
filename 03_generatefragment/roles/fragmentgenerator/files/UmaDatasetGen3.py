#!/usr/bin/env python3

import sys
import traceback
import numpy as np
import os
import psycopg2
import datetime
from tqdm import tqdm

rating_default_value = 1400
statistics_table = 'uma_statistics_02' # 293 cols

def onehot(size, hot_index):
    res = [0] * size
    if hot_index < 0:
        return res
    res[hot_index] = 1
    return res

class IDFilter:
    @classmethod
    def generate_phrase(cls, id):
        return " year='%s' AND monthday='%s' AND jyocd='%s' AND kaiji='%s' AND nichiji='%s' AND racenum='%s'" % id

class DateFilter:
    @classmethod
    def less_than(cls, yearmonthday):
        return " (year<'%s' or (year='%s' AND monthday<'%s'))" % (yearmonthday[:4], yearmonthday[:4], yearmonthday[4:])

    @classmethod
    def less_than_or_equal(cls, yearmonthday):
        return " (year<'%s' or (year='%s' AND monthday<='%s'))" % (yearmonthday[:4], yearmonthday[:4], yearmonthday[4:])

    @classmethod
    def greater_than(cls, yearmonthday):
        return " (year>'%s' or (year='%s' AND monthday>'%s'))" % (yearmonthday[:4], yearmonthday[:4], yearmonthday[4:])

    @classmethod
    def greater_than_or_equal(cls, yearmonthday):
        return " (year>'%s' or (year='%s' AND monthday>='%s'))" % (yearmonthday[:4], yearmonthday[:4], yearmonthday[4:])

def select_query_generate(reference):
    query = 'SELECT ' + reference.cols.strip() + ' FROM ' + reference.table.strip()

    if reference.conditions.strip():
        query += ' WHERE ' + reference.conditions.strip()

    if reference.order.strip():
        query += ' ORDER BY ' + reference.order.strip()

    if reference.limit.strip():
        query += ' LIMIT ' + reference.limit.strip()

    return query

class IDListReference:
    def __init__(self, fromymd, toymd):
        self.table      = 'n_race'
        self.cols       = 'year, monthday, jyocd, kaiji, nichiji, racenum'
        self.conditions = "datakubun='7' AND "\
                            + DateFilter.greater_than_or_equal(fromymd) \
                            + " AND"\
                            + DateFilter.less_than_or_equal(toymd)
        self.order      = 'year ASC, monthday ASC, jyocd ASC, nichiji ASC, racenum ASC'
        self.limit      = ''

class IDListKettonumReference:
    __cols = 'year, monthday, jyocd, kaiji, nichiji, racenum, ijyocd'
    def __init__(self, id, kettonum, limit):
        self.table      = 'n_uma_race'
        self.cols       = IDListKettonumReference.__cols
        self.conditions = "kettonum='%s' AND datakubun='7' AND " % (kettonum,) + DateFilter.less_than(id[0] + id[1])
        self.order      = 'year DESC, monthday DESC, jyocd DESC, nichiji DESC, racenum DESC'
        self.limit      = '%d' % limit

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class kettonumReference:
    __cols = 'kettonum, ijyocd'

    def __init__(self, id):
        self.table      = 'n_uma_race'
        self.cols       = kettonumReference.__cols
        self.conditions = IDFilter.generate_phrase(id) + " AND datakubun='7'"
        self.order      = 'kettonum DESC'
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class HorseInfoReference:
    __cols = 'ijyocd, umaban, sexcd, tozaicd, kisyucode, futan, bataijyu, zogenfugo, zogensa, kakuteijyuni'

    def __init__(self, id, kettonum):
        self.table      = 'n_uma_race'
        self.cols       = HorseInfoReference.__cols
        self.conditions = IDFilter.generate_phrase(id) + " AND kettonum='%s'" % kettonum + " AND datakubun='7'"
        self.order      = 'kettonum DESC'
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class PastHorseInfoReference:
    __cols = 'time, honsyokin, fukasyokin, harontimel3, timediff, kyakusitukubun'
    def __init__(self, id, kettonum):
        self.table      = 'n_uma_race'
        self.cols       = PastHorseInfoReference.__cols
        self.conditions = IDFilter.generate_phrase(id) + " AND kettonum='%s'" % kettonum + " AND datakubun='7'"
        self.order      = 'kettonum DESC'
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class StatisticsReference:
    __cols = 'ruikeihonshiba, '\
'ruikeifukashiba, '\
'ruikeihondirt, '\
'ruikeifukadirt, '\
'ruikeichakukaisu, '\
'chakukaisu1, '\
'chakukaisu2, '\
'chakukaisu3, '\
'chakukaisu4, '\
'chakukaisu5, '\
'chakukaisu6l, '\
'u12shibachakukaisu1, '\
'u12shibachakukaisu2, '\
'u12shibachakukaisu3, '\
'u12shibachakukaisu4, '\
'u12shibachakukaisu5, '\
'u12shibachakukaisu6l, '\
'u14shibachakukaisu1, '\
'u14shibachakukaisu2, '\
'u14shibachakukaisu3, '\
'u14shibachakukaisu4, '\
'u14shibachakukaisu5, '\
'u14shibachakukaisu6l, '\
'u16shibachakukaisu1, '\
'u16shibachakukaisu2, '\
'u16shibachakukaisu3, '\
'u16shibachakukaisu4, '\
'u16shibachakukaisu5, '\
'u16shibachakukaisu6l, '\
'u18shibachakukaisu1, '\
'u18shibachakukaisu2, '\
'u18shibachakukaisu3, '\
'u18shibachakukaisu4, '\
'u18shibachakukaisu5, '\
'u18shibachakukaisu6l, '\
'u20shibachakukaisu1, '\
'u20shibachakukaisu2, '\
'u20shibachakukaisu3, '\
'u20shibachakukaisu4, '\
'u20shibachakukaisu5, '\
'u20shibachakukaisu6l, '\
'u22shibachakukaisu1, '\
'u22shibachakukaisu2, '\
'u22shibachakukaisu3, '\
'u22shibachakukaisu4, '\
'u22shibachakukaisu5, '\
'u22shibachakukaisu6l, '\
'u24shibachakukaisu1, '\
'u24shibachakukaisu2, '\
'u24shibachakukaisu3, '\
'u24shibachakukaisu4, '\
'u24shibachakukaisu5, '\
'u24shibachakukaisu6l, '\
'u28shibachakukaisu1, '\
'u28shibachakukaisu2, '\
'u28shibachakukaisu3, '\
'u28shibachakukaisu4, '\
'u28shibachakukaisu5, '\
'u28shibachakukaisu6l, '\
'o28shibachakukaisu1, '\
'o28shibachakukaisu2, '\
'o28shibachakukaisu3, '\
'o28shibachakukaisu4, '\
'o28shibachakukaisu5, '\
'o28shibachakukaisu6l, '\
'u12dirtchakukaisu1, '\
'u12dirtchakukaisu2, '\
'u12dirtchakukaisu3, '\
'u12dirtchakukaisu4, '\
'u12dirtchakukaisu5, '\
'u12dirtchakukaisu6l, '\
'u14dirtchakukaisu1, '\
'u14dirtchakukaisu2, '\
'u14dirtchakukaisu3, '\
'u14dirtchakukaisu4, '\
'u14dirtchakukaisu5, '\
'u14dirtchakukaisu6l, '\
'u16dirtchakukaisu1, '\
'u16dirtchakukaisu2, '\
'u16dirtchakukaisu3, '\
'u16dirtchakukaisu4, '\
'u16dirtchakukaisu5, '\
'u16dirtchakukaisu6l, '\
'u18dirtchakukaisu1, '\
'u18dirtchakukaisu2, '\
'u18dirtchakukaisu3, '\
'u18dirtchakukaisu4, '\
'u18dirtchakukaisu5, '\
'u18dirtchakukaisu6l, '\
'u20dirtchakukaisu1, '\
'u20dirtchakukaisu2, '\
'u20dirtchakukaisu3, '\
'u20dirtchakukaisu4, '\
'u20dirtchakukaisu5, '\
'u20dirtchakukaisu6l, '\
'u22dirtchakukaisu1, '\
'u22dirtchakukaisu2, '\
'u22dirtchakukaisu3, '\
'u22dirtchakukaisu4, '\
'u22dirtchakukaisu5, '\
'u22dirtchakukaisu6l, '\
'u24dirtchakukaisu1, '\
'u24dirtchakukaisu2, '\
'u24dirtchakukaisu3, '\
'u24dirtchakukaisu4, '\
'u24dirtchakukaisu5, '\
'u24dirtchakukaisu6l, '\
'u28dirtchakukaisu1, '\
'u28dirtchakukaisu2, '\
'u28dirtchakukaisu3, '\
'u28dirtchakukaisu4, '\
'u28dirtchakukaisu5, '\
'u28dirtchakukaisu6l, '\
'o28dirtchakukaisu1, '\
'o28dirtchakukaisu2, '\
'o28dirtchakukaisu3, '\
'o28dirtchakukaisu4, '\
'o28dirtchakukaisu5, '\
'o28dirtchakukaisu6l, '\
'kyakusitukubunkaisu1, '\
'kyakusitukubunkaisu2, '\
'kyakusitukubunkaisu3, '\
'kyakusitukubunkaisu4 '

    def __init__(self, id, kettonum):
        self.table      = statistics_table
        self.cols       = StatisticsReference.__cols
        self.conditions = "kettonum='%s' AND " % (kettonum,) + DateFilter.less_than(id[0] + id[1])
        self.order      = 'year DESC, monthday DESC'
        self.limit      = '1'

    @classmethod
    def size(self):
        return len(self.__cols.strip().split(', '))

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class StaticHorseInfoReference:
    __cols = 'birthdate, hinsyucd'
    def __init__(self, kettonum):
        self.table      = 'n_uma'
        self.cols       = StaticHorseInfoReference.__cols
        self.conditions = 'kettonum=' + "'" + kettonum + "'"
        self.order      = ''
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class KyoriReference: 
    __cols = 'kyori'
    def __init__(self, id):
        self.table      = 'n_race'
        self.cols       = KyoriReference.__cols
        self.conditions = IDFilter.generate_phrase(id) + " AND datakubun='7'"
        self.order      = ''
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class RaceInfoReference: 
    __cols = 'jyocd, jyuryocd, kyori, trackcd, honsyokin1, honsyokin2, honsyokin3, honsyokin4, honsyokin5, honsyokin6, honsyokin7, fukasyokin1, fukasyokin2, fukasyokin3, fukasyokin4, fukasyokin5, tenkocd, sibababacd, dirtbabacd, syussotosu'
    def __init__(self, id):
        self.table      = 'n_race'
        self.cols       = RaceInfoReference.__cols
        self.conditions = IDFilter.generate_phrase(id) + " AND datakubun='7'"
        self.order      = ''
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class HarontimeReference:
    __cols = 'harontimes3, harontimel3'
    def __init__(self, id):
        self.table      = 'n_race'
        self.cols       = HarontimeReference.__cols
        self.conditions = IDFilter.generate_phrase(id) + " AND datakubun='7'"
        self.order      = ''
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class RatingReference:
    __cols = 'year, monthday, rating, ratingdiff'
    def __init__(self, year, monthday, kettonum, limit, rating_table):
        self.table      = rating_table
        self.cols       = self.__cols
        #self.conditions = "kettonum='%s' and concat(year, monthday) < '%s%s'" % (kettonum, year, monthday)
        self.conditions = "kettonum='%s' AND " % (kettonum,) + DateFilter.less_than(year + monthday)
        self.order      = 'year DESC, monthday DESC'
        self.limit      = '%d' % limit

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class Converter:
    @classmethod
    def raceid_to_datetime(cls, raceid):
        return datetime.date(int(raceid[0]), int(raceid[1][:2]), int(raceid[1][2:4]))

    @classmethod
    def ymd_to_datetime(cls, year, monthday):
        return datetime.date(int(year), int(monthday[:2]), int(monthday[2:4]))

    @classmethod
    def birthdate_to_datetime(cls, birthdate):
        return datetime.date(int(birthdate[:4]), int(birthdate[4:6]), int(birthdate[6:8]))

class RaceInfoLoader:
    @classmethod
    def load_data(self, id, everydb):
        with everydb.cursor('evcur') as cur:
            query = select_query_generate(RaceInfoReference(id))
            cur.execute(query)
            rows = cur.fetchall()

        if rows == None:
            raise RuntimeError("Unexpected data shortage of raceinfo")

        elif len(rows) > 1:
            print(query, rows)
            raise RuntimeError("Unexpected data duplication in database")

        row = rows[0]

        jyocd = int(row[RaceInfoReference.index('jyocd')] )
        if jyocd == 0:
            raise RuntimeError("Invalid jyocd")
        jyo = onehot(10, jyocd - 1)

        # 0 : Nodata, 1: Handicap, 2: Secial weight, 3: Weight for age, 4: Special Weight
        jyuryocd    = int(row[RaceInfoReference.index('jyuryocd')])
        if jyuryocd == 0:
            raise RuntimeError("Unexpected data shortage of jyuryocd")
        jyuryo = onehot(4, jyuryocd - 1)

        kyori       = int(row[RaceInfoReference.index('kyori')]) / 1000.0 # km

        # 00: Nodata, 10~22: turf, 23~29 dirt, 51~59 Steeple
        trackcd     = int(row[RaceInfoReference.index('trackcd')])
        if trackcd == 0:
            raise RuntimeError("Unexpected data shortage of trackcd")
        elif trackcd >= 10 and trackcd <= 22:
            track = onehot(3, 0)
        elif trackcd >= 23 and trackcd <= 29:
            track = onehot(3, 1)
        elif trackcd >= 51 and trackcd <= 59:
            track = onehot(3, 2)
            #raise NotImplementedError("trackcd: " + str(trackcd) + " is not implemented")
        else:
            raise NotImplementedError("trackcd: " + str(trackcd) + " is not implemented")

        leftright = [0, 0]
        # turf
        if trackcd == 10:
            leftright[0] = 0
            leftright[1] = 0
        elif trackcd >= 11 and trackcd <= 14:
            leftright[0] = 2 # (left curve 2 times)
            leftright[1] = 0
        elif trackcd >= 15 and trackcd <= 16:
            leftright[0] = 4
            leftright[1] = 0
        elif trackcd >= 17 and trackcd <= 20:
            leftright[0] = 0
            leftright[1] = 2
        elif trackcd >= 21 and trackcd <= 22:
            leftright[0] = 0
            leftright[1] = 4
        # dirt
        elif trackcd == 23 or trackcd == 25 or trackcd == 27:
            leftright[0] = 2 # (left curve 2 times)
            leftright[1] = 0
        elif trackcd == 24 or trackcd == 26 or trackcd == 28:
            leftright[0] = 0 # (left curve 2 times)
            leftright[1] = 2
        # Steeple TBD

        # 0: No data, 1: Sunny, 2: Cloudy, 3: Rain, 4: Light rain, 5: Snow, 6: Light Snow
        tenkocd     = int(row[RaceInfoReference.index('tenkocd')])
        # no data or snow is out of scope
        if tenkocd == 0:
            raise RuntimeError("Unexpected data shortage of tenkocd")
        tenko = onehot(6, tenkocd - 1)

        # 0: No data, 1: Firm, 2: Good, 3: Yielding, 4: Soft
        sibababacd  = int(row[RaceInfoReference.index('sibababacd')])
        dirtbabacd  = int(row[RaceInfoReference.index('dirtbabacd')])

        if sibababacd != 0:
            sibaordirt = onehot(2, 0)
            baba = onehot(4, sibababacd - 1)

        elif dirtbabacd != 0:
            sibaordirt = onehot(2, 1)
            baba = onehot(4, dirtbabacd - 1)

        # priorize dirt if dupricate
        if sibababacd and dirtbabacd :
            pass

        if not sibababacd and not dirtbabacd :
            raise RuntimeError("Unexpected data shortage of baba")

        syussotosu  = int(row[RaceInfoReference.index('syussotosu')])

        return [kyori, syussotosu] + jyuryo + track + leftright + tenko + sibaordirt + baba + jyo

    @classmethod
    def load_data_with_harontime(self, id, everydb):
        data = RaceInfoLoader.load_data(id, everydb)
        with everydb.cursor('evcur') as cur:
            query = select_query_generate(HarontimeReference(id))
            cur.execute(query)
            rows = cur.fetchall()

        if rows == None:
            raise RuntimeError("Unexpected data shortage of raceinfo")

        elif len(rows) > 1:
            print(query, rows)
            raise RuntimeError("Unexpected data duplication in database")

        row = rows[0]
        harontimes3 = int(row[RaceInfoReference.index('harontimes3')]) # 99.9s -> 999
        harontimel3 = int(row[RaceInfoReference.index('harontimel3')])

        return data + [harontimes3, harontimel3]

def load_past_id_from_kettonum(id, kettonum, limit, everydb):
    id_list = list()

    with everydb.cursor('everydb_cur') as everydb_cur:
        # Get race specific uma info from n_race_uma
        query = select_query_generate(IDListKettonumReference(id, kettonum, limit))
        everydb_cur.execute(query)

        while True:
            row = everydb_cur.fetchone()
            if row == None:
                break
            if row[IDListKettonumReference.index('ijyocd')] != '0':
                continue

            id_list.append( row[:6] )

    return id_list

def load_kettonum_list(id, everydb):
    kettonum_list = list()

    with everydb.cursor('everydb_cur') as everydb_cur:
        # Get race specific uma info from n_race_uma
        query = select_query_generate(kettonumReference(id))
        everydb_cur.execute(query)

        while True:
            row = everydb_cur.fetchone()
            if row == None:
                break
            if row[kettonumReference.index('ijyocd')] != '0':
                continue

            kettonum_list.append( row[kettonumReference.index('kettonum')] )

    return kettonum_list

class StatisticsLoader:
    @classmethod
    def load_data(self, id, kettonum, uma_processed):
        query = select_query_generate(StatisticsReference(id, kettonum))
        with uma_processed.cursor('processed') as processed_cur:
            processed_cur.execute(query)
            row = processed_cur.fetchone()

        if row == None:
            row = [0] * StatisticsReference.size()

        # 0.1k yen / 10000000.0 = billion
        ruikeishiba = int(row[StatisticsReference.index('ruikeihonshiba')]) / 10000000.0 \
                     + int(row[StatisticsReference.index('ruikeifukashiba')]) / 10000000.0
        ruikeidirt = int(row[StatisticsReference.index('ruikeihondirt')]) / 10000000.0 \
                     + int(row[StatisticsReference.index('ruikeifukadirt')]) / 10000000.0

        ruikeichakukaisu = int(row[StatisticsReference.index('ruikeichakukaisu')])

        def ratio(row, tag, num):
            head = StatisticsReference.index(tag)
            part = list(map(lambda c: int(c), row[head:head + num]))

            csum = sum(part)

            if csum != 0:
                rto = list(map(lambda c, r=csum: c / r, part))
            else:
                rto = [1.0 / num] * num

            return csum, rto

        chaku, chaku_r = ratio(row, 'chakukaisu1', 6)
        u12sh, u12sh_r = ratio(row, 'u12shibachakukaisu1', 6)
        u14sh, u14sh_r = ratio(row, 'u14shibachakukaisu1', 6)
        u16sh, u16sh_r = ratio(row, 'u16shibachakukaisu1', 6)
        u18sh, u18sh_r = ratio(row, 'u18shibachakukaisu1', 6)
        u20sh, u20sh_r = ratio(row, 'u20shibachakukaisu1', 6)
        u22sh, u22sh_r = ratio(row, 'u22shibachakukaisu1', 6)
        u24sh, u24sh_r = ratio(row, 'u24shibachakukaisu1', 6)
        u28sh, u28sh_r = ratio(row, 'u28shibachakukaisu1', 6)
        o28sh, o28sh_r = ratio(row, 'o28shibachakukaisu1', 6)
        u12di, u12di_r = ratio(row, 'u12dirtchakukaisu1', 6)
        u14di, u14di_r = ratio(row, 'u14dirtchakukaisu1', 6)
        u16di, u16di_r = ratio(row, 'u16dirtchakukaisu1', 6)
        u18di, u18di_r = ratio(row, 'u18dirtchakukaisu1', 6)
        u20di, u20di_r = ratio(row, 'u20dirtchakukaisu1', 6)
        u22di, u22di_r = ratio(row, 'u22dirtchakukaisu1', 6)
        u24di, u24di_r = ratio(row, 'u24dirtchakukaisu1', 6)
        u28di, u28di_r = ratio(row, 'u28dirtchakukaisu1', 6)
        o28di, o28di_r = ratio(row, 'o28dirtchakukaisu1', 6)
        kyaku, kyaku_r = ratio(row, 'kyakusitukubunkaisu1', 4)

        if kyaku == 0:
            kyaku_r = [0.333, 0.333, 0.333, 0.333]

        return [ruikeishiba / 100.0, ruikeidirt/ 100.0, ruikeichakukaisu/ 100.0, chaku/ 100.0, kyaku/ 100.0,
            u12sh/ 100.0, u14sh/ 100.0, u16sh/ 100.0, u18sh/ 100.0, u20sh/ 100.0, u22sh/ 100.0, u24sh/ 100.0, u28sh/ 100.0, o28sh/ 100.0,
            u12di/ 100.0, u14di/ 100.0, u16di/ 100.0, u18di/ 100.0, u20di/ 100.0, u22di/ 100.0, u24di/ 100.0, u28di/ 100.0, o28di/ 100.0,
            ] + chaku_r + kyaku_r +\
            u12sh_r + u14sh_r + u16sh_r + u18sh_r + u20sh_r + u22sh_r + u24sh_r + u28sh_r + o28sh_r +\
            u12di_r + u14di_r + u16di_r + u18di_r + u20di_r + u22di_r + u24di_r + u28di_r + o28di_r

class RatingLoader:
    data_unit_size = 3
    history_limit = 3
    data_size = 3*2*3

    @classmethod
    def pack(self, id, row):
        rating = rating_default_value / 2000.0
        rating_diff = 0
        elapsed_year = 0

        if row:
            rating_date = Converter.ymd_to_datetime(
                            row[RatingReference.index('year')], 
                            row[RatingReference.index('monthday')])
            racedate = Converter.raceid_to_datetime(id)
            elapsed_year = (racedate - rating_date).days / 365
            rating = int(row[RatingReference.index('rating')]) / 2000.0
            rating_diff = int(row[RatingReference.index('ratingdiff')]) / 2000.0

        return [rating, rating_diff, elapsed_year]

    @classmethod
    def load_data(self, id, kettonum, uma_processed):
        shiba_table     = 'uma_rating_20'
        dirt_table      = 'uma_rating_21'

        shiba_rating_list = list()
        dirt_rating_list = list()

        query = select_query_generate(RatingReference(id[0], id[1], kettonum, self.history_limit, shiba_table))
        with uma_processed.cursor('prcur') as processed_cur:
            processed_cur.execute(query)
            rows = processed_cur.fetchall()
        for row in rows:
            shiba_rating_list += self.pack(id, row)

        query = select_query_generate(RatingReference(id[0], id[1], kettonum, self.history_limit, dirt_table))
        with uma_processed.cursor('prcur') as processed_cur:
            processed_cur.execute(query)
            rows = processed_cur.fetchall()
        for row in rows:
            dirt_rating_list += self.pack(id, row)

        ## Padding data
        for i in range(self.history_limit - int(len(shiba_rating_list) / self.data_unit_size)):
            hist_size = len(shiba_rating_list)
            oldest_hist = hist_size - 3
            pad = [1400 / 2000.0, 0, 0] if hist_size == 0 else [shiba_rating_list[oldest_hist], 
                                                        shiba_rating_list[oldest_hist + 1], 
                                                        shiba_rating_list[oldest_hist + 2]]
            shiba_rating_list += pad

        for i in range(self.history_limit - int(len(dirt_rating_list) / self.data_unit_size)):
            hist_size = len(dirt_rating_list)
            oldest_hist = hist_size - 3
            pad = [1400 / 2000.0, 0, 0] if hist_size == 0 else [dirt_rating_list[oldest_hist], 
                                                        dirt_rating_list[oldest_hist + 1], 
                                                        dirt_rating_list[oldest_hist + 2]]
            dirt_rating_list += pad

        return shiba_rating_list + dirt_rating_list

class HorseInfoLoader:
    data_size = 10

    @classmethod
    def load_data(self, id, kettonum, everydb):
        query = select_query_generate(HorseInfoReference(id, kettonum))

        with everydb.cursor('evcur') as everydb_cur:
            everydb_cur.execute(query)

            row = everydb_cur.fetchone()
            if row == None:
                raise RuntimeError("Unexpected data shotage in race_uma")

        ijyocd = HorseInfoReference.index('ijyocd')
        assert ijyocd is 0, "ijyocd true"

        # Convert raw data for learning
        umaban = int(row[HorseInfoReference.index('umaban')] ) / 18.0

        sexcd = int(row[HorseInfoReference.index('sexcd')])
         # 0: Ouma 1: Meuma 2: Senba
        sexoh = onehot(3, sexcd - 1) 

        tozaicd = int(row[HorseInfoReference.index('tozaicd')])
        tozaioh = onehot(2, tozaicd - 1) if tozaicd == 1 or tozaicd == 2 else [0, 0]

        futan = int(row[HorseInfoReference.index('futan')]) / 1000.0 # tonne
        bataijyu = int(row[HorseInfoReference.index('bataijyu')]) / 1000.0 # tonne

        # for processing efficiency, load now for result data
        kakuteijyuni = int(row[HorseInfoReference.index('kakuteijyuni')])

        zogensa = 0 # zogensa is zero when first race 
        zogensa_negative = 0
        if (row[HorseInfoReference.index('zogenfugo')] + row[HorseInfoReference.index('zogensa')]):
            abs_z = int(row[HorseInfoReference.index('zogensa')]) / 1000.0 # tonne
            if row[HorseInfoReference.index('zogenfugo')] == '+':
                zogensa = abs_z
            elif row[HorseInfoReference.index('zogenfugo')] == '-':
                zogensa_negative = abs_z

        return [umaban,] + sexoh + tozaioh + [futan, bataijyu, zogensa, zogensa_negative], kakuteijyuni

class PastHorseInfoLoader:
    data_size = HorseInfoLoader.data_size + 11
    time_normalize = 300
    haronvel_average = 16967.3

    @classmethod
    def load_data(self, id, kettonum, everydb):
        data, kakuteijyuni = HorseInfoLoader.load_data(id, kettonum, everydb)

        with everydb.cursor('evcur') as cur:
            query = select_query_generate(PastHorseInfoReference(id, kettonum))
            cur.execute(query)
            row = cur.fetchone()

        if row == None:
            raise RuntimeError("Unexpected data shortage of uma_race")

        honsyokin = int(row[PastHorseInfoReference.index('honsyokin')]) / 10000000.0 # 0.1k yen / 10000000.0 = billion
        fukasyokin = int(row[PastHorseInfoReference.index('fukasyokin')]) / 10000000.0

        time_min = int(row[PastHorseInfoReference.index('time')][0])
        time_sec = int(row[PastHorseInfoReference.index('time')][1:4]) / 10.0 
        time = (time_min * 60.0 + time_sec) / self.time_normalize 
        timediff = (int(row[PastHorseInfoReference.index('timediff')]) / 10.0) / self.time_normalize
        if timediff < 0:
            timediff = 0

        haron_per_meter = 201.168
        harontimel3_org = int(row[PastHorseInfoReference.index('harontimel3')])
        if harontimel3_org == 0 or harontimel3_org == 999:
            harontimel3_org = 369 # average of harontimel3

        harontimel3 = harontimel3_org / 10.0 / self.time_normalize
        haronvel    = haron_per_meter / harontimel3 * 10 / self.haronvel_average

        kyakusitukubun = onehot(4, int(row[PastHorseInfoReference.index('kyakusitukubun')]) - 1)

        query = select_query_generate(KyoriReference(id))
        with everydb.cursor('evcur') as everydb_cur:
            everydb_cur.execute(query)
            row = everydb_cur.fetchone()
            if row == None:
                raise RuntimeError("Unexpected data shotage in KyoriReference")
        kyori = int(row[0]) / 1000.0 # km
        vel = kyori / (time_min * 60.0 + time_sec)

        return data + [kakuteijyuni / 18, honsyokin + fukasyokin, time, timediff, vel, harontimel3, haronvel] + kyakusitukubun

    @classmethod
    def load_average(self):
        return [7, 0, 100.26 / self.time_normalize, 1.497 / self.time_normalize, 0.016184, 0.12257, 1.0] + [0.25, 0.25, 0.25, 0.25]


class StaticHorseInfoLoader:
    data_size = 1

    @classmethod
    def load_data(self, id, kettonum, everydb):
        with everydb.cursor('evcur') as everydb_cur:
            query = select_query_generate(StaticHorseInfoReference(kettonum))
            everydb_cur.execute(query)
            row = everydb_cur.fetchone()

        if row == None:
            raise RuntimeError("Unexpected data shortage of n_uma")

        racedate = Converter.raceid_to_datetime(id)
        birthdate = Converter.birthdate_to_datetime(row[StaticHorseInfoReference.index('birthdate')])
        liveyear = (racedate - birthdate).days / 365
        return [liveyear]

class PastRaceResultLoader:
    @classmethod
    def load_data(self, id, kettonum, horceinfo, limit, everydb):
        uma_race_result_list = list()
        id_list = load_past_id_from_kettonum(id, kettonum, limit, everydb)

        for past_id in id_list:
            racedate = Converter.raceid_to_datetime(id)
            past_racedate = Converter.raceid_to_datetime(past_id)
            past_days = (racedate - past_racedate).days / 365

            race_result = PastHorseInfoLoader.load_data(past_id, kettonum, everydb)
            uma_race_result_list.append(race_result + [past_days])

        pastrace_len = len(uma_race_result_list)

        if pastrace_len:
            padding = uma_race_result_list[pastrace_len - 1] 
        else:
            padding = horceinfo if not pastrace_len else uma_race_result_list[pastrace_len - 1][0:HorseInfoLoader.data_size]
            padding = padding + PastHorseInfoLoader.load_average() + [0]

        for i in range(limit - len(uma_race_result_list)):
            uma_race_result_list.append(padding)

        return uma_race_result_list

class UmaInfoLoader:
    @classmethod
    def load_data(self, id, kettonum_list, everydb, uma_processed):
        # Get race specific uma info from n_race_uma
        datapack = []
        first_place = []

        for kettonum in kettonum_list:
            uma_race, kakuteijyuni = HorseInfoLoader.load_data(id, kettonum, everydb)
            uma_static = StaticHorseInfoLoader.load_data(id, kettonum, everydb)
            uma_rating = RatingLoader.load_data(id, kettonum, uma_processed)
            uma_statistics = StatisticsLoader.load_data(id, kettonum, uma_processed)

            limit = 3
            uma_pastresult = PastRaceResultLoader.load_data(id, kettonum, uma_race, limit, everydb) 

            # 6 + 1 + 2 + 84 + 16 * 5 = 93 + 16 * 5 + 1= 174
            datapack.append( uma_race 
                            + uma_static 
                            + uma_rating 
                            + uma_statistics 
                            + uma_pastresult[0] 
                            + uma_pastresult[1] 
                            + uma_pastresult[2] 
                            + [1])

            if(kakuteijyuni == 1):
                first_place.append(1)
            else:
                first_place.append(0)

        # padding data
        assert(len(datapack) > 0)
        for i in range(18 - len(datapack)):
            datapack.append( datapack[len(datapack) - 1] )
            first_place.append(0)

        return datapack, first_place

class UmaDatasetGen3:
    def __init__(self):
        try:
            self.con_everydb = psycopg2.connect(os.environ.get('DB_EVERYDB2'))
        except Exception as e:
            print('psycopg2: connecting everydb2 failed')
            raise e

        try:
            self.con_processed = psycopg2.connect(os.environ.get('DB_UMA_PROCESSED'))
        except Exception as e:
            print('psycopg2: connecting uma_processed faied')
            raise e

    def __del__(self):
        self.con_everydb.close()
        self.con_processed.close()

    def __get_race_list_period(self, fromymd, toymd):
        with self.con_everydb.cursor() as cur:
            query = select_query_generate(IDListReference(fromymd, toymd))
            cur.execute(query)
            rows = cur.fetchall()

        return rows

    def load(self, id):
        try:
            kettonum_list = load_kettonum_list(id, self.con_everydb)
        except Exception as e:
            print("failed to load kettonum list : ", e)
            raise e

        try:
            uma_info, first_place = UmaInfoLoader.load_data(id, kettonum_list, self.con_everydb, self.con_processed)
        except Exception as e:
            print("failed to load uma_info : ", e)
            t, v, tb = sys.exc_info()
            for a in traceback.format_exception(t,v,tb): print(a)
            for a in traceback.format_tb(e.__traceback__): print(a)

            raise e

        try:
            race_info = RaceInfoLoader.load_data(id, self.con_everydb)
        except Exception as e:
            print("failed to load race_info : ", e)
            raise e

        packed = [ list() for i in range(19) ]
        packed[0].append(np.array(race_info))
        for i in range(18):
            packed[i + 1].append(np.array(uma_info[i]))

        return packed, first_place

    def load_data(self, fromymd, toymd):
        id_list = self.__get_race_list_period(fromymd, toymd)

        uma_info_list = [list() for i in range(18)]
        first_place_list = list()
        datapack = [list() for i in range(19)]

        for id in tqdm(id_list, desc='Gathering race data'):
            try:
                data, first_place = self.load(id)
            except Exception as e:
                continue

            for dst, src in zip(datapack, data):
                dst.append(src[0])

            first_place_list.append(first_place)

        return datapack, np.array(first_place_list)

if __name__ == "__main__":
    pspr = psqlproxy()
    race, uma, first_place = pspr.load_data('19920000', '19920700')
    print(uma)
    print(race)
    print(first_place)

