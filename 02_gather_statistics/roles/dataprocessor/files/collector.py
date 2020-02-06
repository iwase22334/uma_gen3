#!/usr/bin/env python3
import sys
import os
import psycopg2
import datetime
from collections import OrderedDict
from tqdm import tqdm

tablename = 'uma_statistics_02'

def gen_initial_statistics():
    statistics_list = OrderedDict()

    statistics_list['ruikeihonshiba'] = 0
    statistics_list['ruikeifukashiba'] = 0
    statistics_list['ruikeihondirt'] = 0
    statistics_list['ruikeifukadirt'] = 0
    statistics_list['ruikeihonsyogai'] = 0
    statistics_list['ruikeifukasyogai'] = 0
    statistics_list['ruikeichakukaisu'] = 0
    statistics_list['chakukaisu1'] = 0
    statistics_list['chakukaisu2'] = 0
    statistics_list['chakukaisu3'] = 0
    statistics_list['chakukaisu4'] = 0
    statistics_list['chakukaisu5'] = 0
    statistics_list['chakukaisu6l'] = 0
    statistics_list['ryoshibachakukaisu1'] = 0 
    statistics_list['ryoshibachakukaisu2'] = 0
    statistics_list['ryoshibachakukaisu3'] = 0
    statistics_list['ryoshibachakukaisu4'] = 0
    statistics_list['ryoshibachakukaisu5'] = 0
    statistics_list['ryoshibachakukaisu6l'] = 0
    statistics_list['yayaomoshibachakukaisu1'] = 0
    statistics_list['yayaomoshibachakukaisu2'] = 0
    statistics_list['yayaomoshibachakukaisu3'] = 0
    statistics_list['yayaomoshibachakukaisu4'] = 0
    statistics_list['yayaomoshibachakukaisu5'] = 0
    statistics_list['yayaomoshibachakukaisu6l'] = 0
    statistics_list['omoshibachakukaisu1'] = 0
    statistics_list['omoshibachakukaisu2'] = 0
    statistics_list['omoshibachakukaisu3'] = 0
    statistics_list['omoshibachakukaisu4'] = 0
    statistics_list['omoshibachakukaisu5'] = 0
    statistics_list['omoshibachakukaisu6l'] = 0
    statistics_list['furyoshibachakukaisu1'] = 0
    statistics_list['furyoshibachakukaisu2'] = 0
    statistics_list['furyoshibachakukaisu3'] = 0
    statistics_list['furyoshibachakukaisu4'] = 0
    statistics_list['furyoshibachakukaisu5'] = 0
    statistics_list['furyoshibachakukaisu6l'] = 0
    statistics_list['ryodirtchakukaisu1'] = 0 
    statistics_list['ryodirtchakukaisu2'] = 0
    statistics_list['ryodirtchakukaisu3'] = 0
    statistics_list['ryodirtchakukaisu4'] = 0
    statistics_list['ryodirtchakukaisu5'] = 0
    statistics_list['ryodirtchakukaisu6l'] = 0
    statistics_list['yayaomodirtchakukaisu1'] = 0
    statistics_list['yayaomodirtchakukaisu2'] = 0
    statistics_list['yayaomodirtchakukaisu3'] = 0
    statistics_list['yayaomodirtchakukaisu4'] = 0
    statistics_list['yayaomodirtchakukaisu5'] = 0
    statistics_list['yayaomodirtchakukaisu6l'] = 0
    statistics_list['omodirtchakukaisu1'] = 0
    statistics_list['omodirtchakukaisu2'] = 0
    statistics_list['omodirtchakukaisu3'] = 0
    statistics_list['omodirtchakukaisu4'] = 0
    statistics_list['omodirtchakukaisu5'] = 0
    statistics_list['omodirtchakukaisu6l'] = 0
    statistics_list['furyodirtchakukaisu1'] = 0
    statistics_list['furyodirtchakukaisu2'] = 0
    statistics_list['furyodirtchakukaisu3'] = 0
    statistics_list['furyodirtchakukaisu4'] = 0
    statistics_list['furyodirtchakukaisu5'] = 0
    statistics_list['furyodirtchakukaisu6l'] = 0
    statistics_list['ryosyogaichakukaisu1'] = 0 
    statistics_list['ryosyogaichakukaisu2'] = 0
    statistics_list['ryosyogaichakukaisu3'] = 0
    statistics_list['ryosyogaichakukaisu4'] = 0
    statistics_list['ryosyogaichakukaisu5'] = 0
    statistics_list['ryosyogaichakukaisu6l'] = 0
    statistics_list['yayaomosyogaichakukaisu1'] = 0
    statistics_list['yayaomosyogaichakukaisu2'] = 0
    statistics_list['yayaomosyogaichakukaisu3'] = 0
    statistics_list['yayaomosyogaichakukaisu4'] = 0
    statistics_list['yayaomosyogaichakukaisu5'] = 0
    statistics_list['yayaomosyogaichakukaisu6l'] = 0
    statistics_list['omosyogaichakukaisu1'] = 0
    statistics_list['omosyogaichakukaisu2'] = 0
    statistics_list['omosyogaichakukaisu3'] = 0
    statistics_list['omosyogaichakukaisu4'] = 0
    statistics_list['omosyogaichakukaisu5'] = 0
    statistics_list['omosyogaichakukaisu6l'] = 0
    statistics_list['furyosyogaichakukaisu1'] = 0
    statistics_list['furyosyogaichakukaisu2'] = 0
    statistics_list['furyosyogaichakukaisu3'] = 0
    statistics_list['furyosyogaichakukaisu4'] = 0
    statistics_list['furyosyogaichakukaisu5'] = 0
    statistics_list['furyosyogaichakukaisu6l'] = 0
    statistics_list['sshibachakukaisu1'] = 0
    statistics_list['sshibachakukaisu2'] = 0
    statistics_list['sshibachakukaisu3'] = 0
    statistics_list['sshibachakukaisu4'] = 0
    statistics_list['sshibachakukaisu5'] = 0
    statistics_list['sshibachakukaisu6l'] = 0
    statistics_list['rshibachakukaisu1'] = 0
    statistics_list['rshibachakukaisu2'] = 0
    statistics_list['rshibachakukaisu3'] = 0
    statistics_list['rshibachakukaisu4'] = 0
    statistics_list['rshibachakukaisu5'] = 0
    statistics_list['rshibachakukaisu6l'] = 0
    statistics_list['lshibachakukaisu1'] = 0
    statistics_list['lshibachakukaisu2'] = 0
    statistics_list['lshibachakukaisu3'] = 0
    statistics_list['lshibachakukaisu4'] = 0
    statistics_list['lshibachakukaisu5'] = 0
    statistics_list['lshibachakukaisu6l'] = 0
    statistics_list['sdirtchakukaisu1'] = 0
    statistics_list['sdirtchakukaisu2'] = 0
    statistics_list['sdirtchakukaisu3'] = 0
    statistics_list['sdirtchakukaisu4'] = 0
    statistics_list['sdirtchakukaisu5'] = 0
    statistics_list['sdirtchakukaisu6l'] = 0
    statistics_list['rdirtchakukaisu1'] = 0
    statistics_list['rdirtchakukaisu2'] = 0
    statistics_list['rdirtchakukaisu3'] = 0
    statistics_list['rdirtchakukaisu4'] = 0
    statistics_list['rdirtchakukaisu5'] = 0
    statistics_list['rdirtchakukaisu6l'] = 0
    statistics_list['ldirtchakukaisu1'] = 0
    statistics_list['ldirtchakukaisu2'] = 0
    statistics_list['ldirtchakukaisu3'] = 0
    statistics_list['ldirtchakukaisu4'] = 0
    statistics_list['ldirtchakukaisu5'] = 0
    statistics_list['ldirtchakukaisu6l'] = 0
    statistics_list['u12shibachakukaisu1'] = 0
    statistics_list['u12shibachakukaisu2'] = 0
    statistics_list['u12shibachakukaisu3'] = 0
    statistics_list['u12shibachakukaisu4'] = 0
    statistics_list['u12shibachakukaisu5'] = 0
    statistics_list['u12shibachakukaisu6l'] = 0
    statistics_list['u14shibachakukaisu1'] = 0
    statistics_list['u14shibachakukaisu2'] = 0
    statistics_list['u14shibachakukaisu3'] = 0
    statistics_list['u14shibachakukaisu4'] = 0
    statistics_list['u14shibachakukaisu5'] = 0
    statistics_list['u14shibachakukaisu6l'] = 0
    statistics_list['u16shibachakukaisu1'] = 0
    statistics_list['u16shibachakukaisu2'] = 0
    statistics_list['u16shibachakukaisu3'] = 0
    statistics_list['u16shibachakukaisu4'] = 0
    statistics_list['u16shibachakukaisu5'] = 0
    statistics_list['u16shibachakukaisu6l'] = 0
    statistics_list['u18shibachakukaisu1'] = 0
    statistics_list['u18shibachakukaisu2'] = 0
    statistics_list['u18shibachakukaisu3'] = 0
    statistics_list['u18shibachakukaisu4'] = 0
    statistics_list['u18shibachakukaisu5'] = 0
    statistics_list['u18shibachakukaisu6l'] = 0
    statistics_list['u20shibachakukaisu1'] = 0
    statistics_list['u20shibachakukaisu2'] = 0
    statistics_list['u20shibachakukaisu3'] = 0
    statistics_list['u20shibachakukaisu4'] = 0
    statistics_list['u20shibachakukaisu5'] = 0
    statistics_list['u20shibachakukaisu6l'] = 0
    statistics_list['u22shibachakukaisu1'] = 0
    statistics_list['u22shibachakukaisu2'] = 0
    statistics_list['u22shibachakukaisu3'] = 0
    statistics_list['u22shibachakukaisu4'] = 0
    statistics_list['u22shibachakukaisu5'] = 0
    statistics_list['u22shibachakukaisu6l'] = 0
    statistics_list['u24shibachakukaisu1'] = 0
    statistics_list['u24shibachakukaisu2'] = 0
    statistics_list['u24shibachakukaisu3'] = 0
    statistics_list['u24shibachakukaisu4'] = 0
    statistics_list['u24shibachakukaisu5'] = 0
    statistics_list['u24shibachakukaisu6l'] = 0
    statistics_list['u28shibachakukaisu1'] = 0
    statistics_list['u28shibachakukaisu2'] = 0
    statistics_list['u28shibachakukaisu3'] = 0
    statistics_list['u28shibachakukaisu4'] = 0
    statistics_list['u28shibachakukaisu5'] = 0
    statistics_list['u28shibachakukaisu6l'] = 0
    statistics_list['o28shibachakukaisu1'] = 0
    statistics_list['o28shibachakukaisu2'] = 0
    statistics_list['o28shibachakukaisu3'] = 0
    statistics_list['o28shibachakukaisu4'] = 0
    statistics_list['o28shibachakukaisu5'] = 0
    statistics_list['o28shibachakukaisu6l'] = 0
    statistics_list['u12dirtchakukaisu1'] = 0
    statistics_list['u12dirtchakukaisu2'] = 0
    statistics_list['u12dirtchakukaisu3'] = 0
    statistics_list['u12dirtchakukaisu4'] = 0
    statistics_list['u12dirtchakukaisu5'] = 0
    statistics_list['u12dirtchakukaisu6l'] = 0
    statistics_list['u14dirtchakukaisu1'] = 0
    statistics_list['u14dirtchakukaisu2'] = 0
    statistics_list['u14dirtchakukaisu3'] = 0
    statistics_list['u14dirtchakukaisu4'] = 0
    statistics_list['u14dirtchakukaisu5'] = 0
    statistics_list['u14dirtchakukaisu6l'] = 0
    statistics_list['u16dirtchakukaisu1'] = 0
    statistics_list['u16dirtchakukaisu2'] = 0
    statistics_list['u16dirtchakukaisu3'] = 0
    statistics_list['u16dirtchakukaisu4'] = 0
    statistics_list['u16dirtchakukaisu5'] = 0
    statistics_list['u16dirtchakukaisu6l'] = 0
    statistics_list['u18dirtchakukaisu1'] = 0
    statistics_list['u18dirtchakukaisu2'] = 0
    statistics_list['u18dirtchakukaisu3'] = 0
    statistics_list['u18dirtchakukaisu4'] = 0
    statistics_list['u18dirtchakukaisu5'] = 0
    statistics_list['u18dirtchakukaisu6l'] = 0
    statistics_list['u20dirtchakukaisu1'] = 0
    statistics_list['u20dirtchakukaisu2'] = 0
    statistics_list['u20dirtchakukaisu3'] = 0
    statistics_list['u20dirtchakukaisu4'] = 0
    statistics_list['u20dirtchakukaisu5'] = 0
    statistics_list['u20dirtchakukaisu6l'] = 0
    statistics_list['u22dirtchakukaisu1'] = 0
    statistics_list['u22dirtchakukaisu2'] = 0
    statistics_list['u22dirtchakukaisu3'] = 0
    statistics_list['u22dirtchakukaisu4'] = 0
    statistics_list['u22dirtchakukaisu5'] = 0
    statistics_list['u22dirtchakukaisu6l'] = 0
    statistics_list['u24dirtchakukaisu1'] = 0
    statistics_list['u24dirtchakukaisu2'] = 0
    statistics_list['u24dirtchakukaisu3'] = 0
    statistics_list['u24dirtchakukaisu4'] = 0
    statistics_list['u24dirtchakukaisu5'] = 0
    statistics_list['u24dirtchakukaisu6l'] = 0
    statistics_list['u28dirtchakukaisu1'] = 0
    statistics_list['u28dirtchakukaisu2'] = 0
    statistics_list['u28dirtchakukaisu3'] = 0
    statistics_list['u28dirtchakukaisu4'] = 0
    statistics_list['u28dirtchakukaisu5'] = 0
    statistics_list['u28dirtchakukaisu6l'] = 0
    statistics_list['o28dirtchakukaisu1'] = 0
    statistics_list['o28dirtchakukaisu2'] = 0
    statistics_list['o28dirtchakukaisu3'] = 0
    statistics_list['o28dirtchakukaisu4'] = 0
    statistics_list['o28dirtchakukaisu5'] = 0
    statistics_list['o28dirtchakukaisu6l'] = 0
    statistics_list['jyo01syogaichakukaisu1'] = 0
    statistics_list['jyo01syogaichakukaisu2'] = 0
    statistics_list['jyo01syogaichakukaisu3'] = 0
    statistics_list['jyo01syogaichakukaisu4'] = 0
    statistics_list['jyo01syogaichakukaisu5'] = 0
    statistics_list['jyo01syogaichakukaisu6l'] = 0
    statistics_list['jyo02syogaichakukaisu1'] = 0
    statistics_list['jyo02syogaichakukaisu2'] = 0
    statistics_list['jyo02syogaichakukaisu3'] = 0
    statistics_list['jyo02syogaichakukaisu4'] = 0
    statistics_list['jyo02syogaichakukaisu5'] = 0
    statistics_list['jyo02syogaichakukaisu6l'] = 0
    statistics_list['jyo03syogaichakukaisu1'] = 0
    statistics_list['jyo03syogaichakukaisu2'] = 0
    statistics_list['jyo03syogaichakukaisu3'] = 0
    statistics_list['jyo03syogaichakukaisu4'] = 0
    statistics_list['jyo03syogaichakukaisu5'] = 0
    statistics_list['jyo03syogaichakukaisu6l'] = 0
    statistics_list['jyo04syogaichakukaisu1'] = 0
    statistics_list['jyo04syogaichakukaisu2'] = 0
    statistics_list['jyo04syogaichakukaisu3'] = 0
    statistics_list['jyo04syogaichakukaisu4'] = 0
    statistics_list['jyo04syogaichakukaisu5'] = 0
    statistics_list['jyo04syogaichakukaisu6l'] = 0
    statistics_list['jyo05syogaichakukaisu1'] = 0
    statistics_list['jyo05syogaichakukaisu2'] = 0
    statistics_list['jyo05syogaichakukaisu3'] = 0
    statistics_list['jyo05syogaichakukaisu4'] = 0
    statistics_list['jyo05syogaichakukaisu5'] = 0
    statistics_list['jyo05syogaichakukaisu6l'] = 0
    statistics_list['jyo06syogaichakukaisu1'] = 0
    statistics_list['jyo06syogaichakukaisu2'] = 0
    statistics_list['jyo06syogaichakukaisu3'] = 0
    statistics_list['jyo06syogaichakukaisu4'] = 0
    statistics_list['jyo06syogaichakukaisu5'] = 0
    statistics_list['jyo06syogaichakukaisu6l'] = 0
    statistics_list['jyo07syogaichakukaisu1'] = 0
    statistics_list['jyo07syogaichakukaisu2'] = 0
    statistics_list['jyo07syogaichakukaisu3'] = 0
    statistics_list['jyo07syogaichakukaisu4'] = 0
    statistics_list['jyo07syogaichakukaisu5'] = 0
    statistics_list['jyo07syogaichakukaisu6l'] = 0
    statistics_list['jyo08syogaichakukaisu1'] = 0
    statistics_list['jyo08syogaichakukaisu2'] = 0
    statistics_list['jyo08syogaichakukaisu3'] = 0
    statistics_list['jyo08syogaichakukaisu4'] = 0
    statistics_list['jyo08syogaichakukaisu5'] = 0
    statistics_list['jyo08syogaichakukaisu6l'] = 0
    statistics_list['jyo09syogaichakukaisu1'] = 0
    statistics_list['jyo09syogaichakukaisu2'] = 0
    statistics_list['jyo09syogaichakukaisu3'] = 0
    statistics_list['jyo09syogaichakukaisu4'] = 0
    statistics_list['jyo09syogaichakukaisu5'] = 0
    statistics_list['jyo09syogaichakukaisu6l'] = 0
    statistics_list['jyo10syogaichakukaisu1'] = 0
    statistics_list['jyo10syogaichakukaisu2'] = 0
    statistics_list['jyo10syogaichakukaisu3'] = 0
    statistics_list['jyo10syogaichakukaisu4'] = 0
    statistics_list['jyo10syogaichakukaisu5'] = 0
    statistics_list['jyo10syogaichakukaisu6l'] = 0
    statistics_list['kyakusitukubunkaisu1'] = 0
    statistics_list['kyakusitukubunkaisu2'] = 0
    statistics_list['kyakusitukubunkaisu3'] = 0
    statistics_list['kyakusitukubunkaisu4'] = 0

    return statistics_list

def increment(statistics, key):
    statistics[key] = statistics[key] + 1

def add(statistics, key, val):
    statistics[key] = statistics[key] + val

def update_statistics(statistics, race_info, kakuteijyuni_str, kyakusitukubun_str):
    trackcd         = int(race_info[RaceInfoReference.index('trackcd')])
    jyocd           = race_info[RaceInfoReference.index('jyocd')]
    kyakusitukubun  = int(kyakusitukubun_str)

    kakuteijyuni    = int(kakuteijyuni_str)
    if kakuteijyuni == 0:
        raise RuntimeError("Unexpected kakuteijyuni: 0")

    babacd = race_info[RaceInfoReference.index('sibababacd')]
    if babacd == '0':
       babacd = race_info[RaceInfoReference.index('dirtbabacd')]

    if babacd == '0':
        raise RuntimeError("Unexpected babacd: 0")

    if babacd == '1':
        babakey = 'ryo'
    elif babacd == '2':
        babakey = 'yayaomo'
    elif babacd == '3':
        babakey = 'omo'
    elif babacd == '4':
        babakey = 'furyo'

    kyori = int(race_info[RaceInfoReference.index('kyori')])
    if kyori <= 1200:
        kyorikey = 'u12'
    elif kyori <= 1400:
        kyorikey = 'u14'
    elif kyori <= 1600:
        kyorikey = 'u16'
    elif kyori <= 1800:
        kyorikey = 'u18'
    elif kyori <= 2000:
        kyorikey = 'u20'
    elif kyori <= 2200:
        kyorikey = 'u22'
    elif kyori <= 2400:
        kyorikey = 'u24'
    elif kyori <= 2800:
        kyorikey = 'u28'
    elif kyori > 2800:
        kyorikey = 'o28'

    if trackcd == 0:
        raise RuntimeError("Unexpected data shortage of trackcd")
    elif trackcd >= 10 and trackcd <= 22:
        trackkey = 'shiba'
    elif trackcd >= 23 and trackcd <= 29:
        trackkey = 'dirt'
    elif trackcd >= 51 and trackcd <= 59:
        trackkey = 'syogai'
    else:
        raise NotImplementedError("trackcd: " + str(trackcd) + " is not implemented")

    # turf
    if trackcd == 10:
        lrkey = 's'
    elif trackcd >= 11 and trackcd <= 16:
        lrkey = 'l'
    elif trackcd >= 17 and trackcd <= 22:
        lrkey = 'r'
    # dirt
    elif trackcd == 29:
        lrkey = 's'
    elif trackcd == 23 or trackcd == 25 or trackcd == 27:
        lrkey = 'l'
    elif trackcd == 24 or trackcd == 26 or trackcd == 28:
        lrkey = 'r'

    jyunikey = str(kakuteijyuni)
    if kakuteijyuni > 5:
        jyunikey = '6l'

    honsyokin = 0
    fukasyokin = 0
    if kakuteijyuni <= 5:
        honsyokin_str = race_info[RaceInfoReference.index('honsyokin%d' % (kakuteijyuni,))]
        honsyokin = int(honsyokin_str) if not honsyokin_str is None else 0
        fukasyokin_str = race_info[RaceInfoReference.index('fukasyokin%d' % (kakuteijyuni,))]
        fukasyokin = int(fukasyokin_str) if not fukasyokin_str is None else 0

    # syokin
    add(statistics, 'ruikeihon%s' % (trackkey,), honsyokin)
    add(statistics, 'ruikeifuka%s' % (trackkey,), fukasyokin)
    increment(statistics, 'ruikeichakukaisu')
    increment(statistics, 'chakukaisu%s' % (jyunikey,))
    increment(statistics, '%s%schakukaisu%s' % (babakey, trackkey, jyunikey,))

    if trackkey == 'shiba' or trackkey == 'dirt':
        increment(statistics, '%s%schakukaisu%s' % (lrkey, trackkey, jyunikey,))
        increment(statistics, '%s%schakukaisu%s' % (kyorikey, trackkey, jyunikey,))
    elif trackkey == 'syogai':
        if int(jyocd) <= 10:
            increment(statistics, 'jyo%s%schakukaisu%s' % (jyocd, trackkey, jyunikey,))

    # kyakusitu
    if kyakusitukubun > 0:
        increment(statistics, 'kyakusitukubunkaisu%d' % (kyakusitukubun,))

class IDFilter:
    @classmethod
    def generate_phrase(cls, id):
        return " year='%s' AND monthday='%s' AND jyocd='%s' AND kaiji='%s' AND nichiji='%s' AND racenum='%s'" % id

class IDFilterUntilToday:
    @classmethod
    def generate_phrase(cls, id):
        #return " concat(year, monthday)<'%s'" % (id[0] + id[1],)
        return " (year<'%s' or (year='%s' AND monthday<'%s'))" % (id[0], id[0], id[1])

class DateFilter:
    @classmethod
    def generate_condition_lesser_days(cls, yearmonthday):
        return " (year<'%s' or (year='%s' AND monthday<'%s'))" % (yearmonthday[:4], yearmonthday[:4], yearmonthday[4:])

    @classmethod
    def generate_condition_greater_days(cls, yearmonthday):
        return " (year>'%s' or (year='%s' AND monthday>'%s'))" % (yearmonthday[:4], yearmonthday[:4], yearmonthday[4:])

    @classmethod
    def generate_condition_newer_days(cls, yearmonthday):
        #return " concat(year, monthday)>='%s'" % yearmonthday
        return " (year>'%s' or (year='%s' AND monthday>='%s'))" % (yearmonthday[:4], yearmonthday[:4], yearmonthday[4:])

    @classmethod
    def generate_condition_older_days(cls, yearmonthday):
        #return " concat(year, monthday)<='%s'" % yearmonthday
        return " (year<'%s' or (year='%s' AND monthday<='%s'))" % (yearmonthday[:4], yearmonthday[:4], yearmonthday[4:])

class SelectPhrase:
    @classmethod
    def generate(self, reference):
        query = 'SELECT ' + reference.cols.strip() + ' FROM ' + reference.table.strip()

        if reference.conditions.strip():
            query += ' WHERE ' + reference.conditions.strip()

        if reference.order.strip():
            query += ' ORDER BY ' + reference.order.strip()

        if reference.limit.strip():
            query += ' LIMIT ' + reference.limit.strip()

        return query

class InsertPhrase:
    @classmethod
    def generate(self, id, kettonum, statistics):
        str =  "INSERT INTO %s VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s'" % ((tablename,) + id + (kettonum,))

        for value in list(statistics.values()):
            str = str + ", '%d'" % value

        str = str + ");"
        return str

class IDListReference:
    def __init__(self, fromyearmonthday, toyearmonthday):
        self.table      = 'n_race'
        self.cols       = 'year, monthday, jyocd, kaiji, nichiji, racenum'
        self.conditions = "datakubun='7'" + ' AND' + DateFilter.generate_condition_newer_days(fromyearmonthday) + ' AND' + DateFilter.generate_condition_older_days(toyearmonthday)
        self.order      = 'year ASC, monthday ASC, jyocd ASC, nichiji ASC, racenum ASC'
        self.limit      = ''
        #self.limit      = '3'

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
    __cols =  'year, monthday, jyocd, kaiji, nichiji, racenum, ijyocd, kakuteijyuni, kyakusitukubun'

    def __init__(self, id, fromymd, kettonum):
        self.table      = 'n_uma_race'
        self.cols       = HorseInfoReference.__cols
        if fromymd is None:
            #self.conditions = "datakubun='7' AND concat(year, monthday) <= '%s' AND kettonum='%s'" % (id[0] + id[1], kettonum) 
            self.conditions = "datakubun='7' AND kettonum='%s' AND" % (kettonum,) \
                                + DateFilter.generate_condition_older_days(id[0]+id[1])
        else:
            #self.conditions = "datakubun='7' AND concat(year, monthday) <= '%s' AND concat(year, monthday) > '%s' AND kettonum='%s'" % (id[0] + id[1], fromymd, kettonum) 
            self.conditions = "datakubun='7' AND kettonum='%s' AND" % (kettonum,) \
                                + DateFilter.generate_condition_older_days(id[0]+id[1]) \
                                + " AND" \
                                + DateFilter.generate_condition_greater_days(id[0]+id[1]) 

        self.order      = 'year ASC, monthday ASC, jyocd ASC, nichiji ASC, racenum ASC'
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class RaceInfoReference:
    __cols = 'jyocd, kyori, trackcd, honsyokin1, honsyokin2, honsyokin3, honsyokin4, honsyokin5, honsyokin6, honsyokin7, fukasyokin1, fukasyokin2, fukasyokin3, fukasyokin4, fukasyokin5, sibababacd, dirtbabacd'

    def __init__(self, id):
        self.table      = 'n_race'
        self.cols       = RaceInfoReference.__cols
        self.conditions = "datakubun='7' AND " + IDFilter.generate_phrase(id)
        self.order      = 'year ASC, monthday ASC, jyocd ASC, nichiji ASC, racenum ASC'
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class IsExistsStatisticsReference:
    __cols =  '1'

    def __init__(self, id, kettonum):
        self.table      = tablename
        self.cols       = IsExistsStatisticsReference.__cols
        self.conditions = IDFilter.generate_phrase(id) + " AND kettonum='%s'" % kettonum
        self.order      = ''
        self.limit      = ''

class LatestStatisticsReference:
    __cols =  '*'

    def __init__(self, id, kettonum):
        self.table      = tablename
        self.cols       = LatestStatisticsReference.__cols
        #self.conditions = "kettonum='%s' AND concat(year, monthday) < '%s%s'" % (kettonum, id[0], id[1])
        self.conditions = "kettonum='%s' AND " % (kettonum,) + DateFilter.generate_condition_lesser_days( id[0] + id[1] )
        self.order      = 'year DESC, monthday DESC, jyocd DESC, nichiji DESC, racenum DESC'
        self.limit      = '1'

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class IDReader:
    @classmethod
    def load_data(self, fromyear, toyear, connection):
        with connection.cursor('id_cursor') as cur:
            query = SelectPhrase.generate(IDListReference(fromyear, toyear))
            cur.execute(query)
            id_list  = cur.fetchall()

        return id_list

def load_kettonum_list(id, everydb):
    with everydb.cursor('everydb_cur') as everydb_cur:
        # Get race specific uma info from n_race_uma
        query = SelectPhrase.generate(kettonumReference(id))
        everydb_cur.execute(query)

        kettonum_list = []

        while True:
            row = everydb_cur.fetchone()
            if row == None:
                break
            if row[kettonumReference.index('ijyocd')] != '0':
                continue

            kettonum_list.append( row[kettonumReference.index('kettonum')] )

        return kettonum_list

def is_exists_statistics(id, kettonum, uma_processed):
    with uma_processed.cursor('uma_processed_cur') as up_cur:
        # Get race specific uma info from n_race_uma
        query = SelectPhrase.generate(IsExistsStatisticsReference(id, kettonum))
        up_cur.execute(query)
        row = up_cur.fetchone()

    return row

def load_latest_statistics(id, kettonum, uma_processed):
    with uma_processed.cursor('uma_processed_cur') as up_cur:
        # Get race specific uma info from n_race_uma
        query = SelectPhrase.generate(LatestStatisticsReference(id, kettonum))
        up_cur.execute(query)
        row = up_cur.fetchone()

    return row

def load_past_uma_race_list(id, fromymd, kettonum, everydb):
    with everydb.cursor('everydb_cur') as everydb_cur:
        # Get race specific uma info from n_race_uma
        query = SelectPhrase.generate(HorseInfoReference(id, fromymd, kettonum))
        everydb_cur.execute(query)

        id_list = []
        kakuteijyuni_list = []
        kyakusitukubun_list = []

        while True:
            row = everydb_cur.fetchone()
            if row == None:
                break
            if row[HorseInfoReference.index('ijyocd')] != '0':
                continue

            id_list.append(( row[HorseInfoReference.index('year')],
                             row[HorseInfoReference.index('monthday')],
                             row[HorseInfoReference.index('jyocd')],
                             row[HorseInfoReference.index('kaiji')],
                             row[HorseInfoReference.index('nichiji')],
                             row[HorseInfoReference.index('racenum')]))

            kakuteijyuni_list.append( row[HorseInfoReference.index('kakuteijyuni')] )
            kyakusitukubun_list.append( row[HorseInfoReference.index('kyakusitukubun')] )

        return id_list, kakuteijyuni_list, kyakusitukubun_list

def load_race_info(id, everydb):
    with everydb.cursor('everydb_cur') as everydb_cur:
        # Get race specific uma info from n_race_uma
        query = SelectPhrase.generate(RaceInfoReference(id))
        everydb_cur.execute(query)
        row = everydb_cur.fetchone()
        if row == None:
            raise RuntimeError("Unexpected data shortage of raceinfo")
        return row

def save_statistics(id, kettonum, statistics, connection):
    with connection.cursor() as cur:
        query = InsertPhrase.generate(id, kettonum, statistics)
        cur.execute(query)
    connection.commit()

class StatisticsUpdator:
    def __init__(self):
        try:
            self.connection_raw  = psycopg2.connect(os.environ.get('DB_EVERYDB2'), sslmode='disable')
        except:
            print('psycopg2: opening connection 01 faied')
            sys.exit(0)

        try:
            self.connection_processed = psycopg2.connect(os.environ.get('DB_UMA_PROCESSED'), sslmode='disable')
        except:
            print('psycopg2: opening connection 02 faied')
            sys.exit(0)

    def __del__(self):
        self.connection_raw.close()
        self.connection_processed.close()

    def process(self, fromyearmonthday, toyearmonthday):
        id_list = IDReader.load_data(fromyearmonthday, toyearmonthday, self.connection_raw)

        for id in tqdm(id_list, desc='Gathering race data'):
            print('\nprocessing id: %s%s%s%s%s%s' % id, end='\033[1A\r', flush=True)

            try:
                kettonum_list = load_kettonum_list(id, self.connection_raw)
            except RuntimeError as e:
                print(e)
                continue

            for kettonum in kettonum_list:
                if is_exists_statistics(id, kettonum, self.connection_processed):
                    print("already exists: ", id, kettonum)
                    continue

                statistics_row = load_latest_statistics(id, kettonum, self.connection_processed)
                latest_statistics = gen_initial_statistics()

                if not statistics_row is None:
                    for key, i in zip(latest_statistics.keys(), range(len(latest_statistics))):
                        latest_statistics[key] = statistics_row[7 + i]
                    last_race_date = statistics_row[0] + statistics_row[1]

                else:
                    last_race_date = None

                past_id_list, kakuteijyuni_list, kyakusitukubun_list = load_past_uma_race_list(id, last_race_date, kettonum, self.connection_raw)
                for pastid, kakuteijyuni, kyakusitukubun in zip(past_id_list, kakuteijyuni_list, kyakusitukubun_list):
                    try:
                        race_info = load_race_info(pastid, self.connection_raw)
                    except RuntimeError as e:
                        print(e)
                        continue

                    try:
                        update_statistics(latest_statistics, race_info, kakuteijyuni, kyakusitukubun)
                    except RuntimeError as e:
                        print(e)
                        continue

                try:
                    save_statistics(id, kettonum, latest_statistics, self.connection_processed)
                except RuntimeError as e:
                    print(e)
                    exit()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("usage: collector.py fromymd toymd")
        exit()

    fromymd = sys.argv[1]
    toymd = sys.argv[2]

    updator = StatisticsUpdator()

    print("src: ", os.environ.get('DB_EVERYDB2'))
    print("dst: ", os.environ.get('DB_UMA_PROCESSED'))
    print(fromymd, "~", toymd)

    updator.process(fromymd, toymd)

    print("complete")

    #updator.process('19970320', '20200000')
    #updator.process('19900000', '20200000')
    #updator.process('19990000', '20100000')
    #updator.process('20100000', '20200000')

