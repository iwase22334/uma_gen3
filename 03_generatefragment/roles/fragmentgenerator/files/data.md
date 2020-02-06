## HorseInfo  

| name             | type   | unit  | range  |
|------------------|--------|-------|--------|
| umaban           | int    |       | [1-18] |
| sexcd            | bin[4] |       |        |
| tozaicd          | bin[5] |       |        |
| futan            | float  | tonne | (0-1)  |
| bataijyu         | float  | tonne | (0-1)  |
| zogensa          | float  | tonne | [0-1)  |
| zogensa_negative | float  | tonne | [0-1)  |

## PastHorseInfo  

| name           | type      | unit    | range          |
|----------------|-----------|---------|----------------|
| HorseInfo      | HorseInfo |         |                |
| honsyokin      | int       | billion | 0 or more      |
| fukasyokin     | int       | billion | 0 or more      |
| time           | float     | sec/300 | greater than 0 |
| timediff       | float     | sec/300 | 0 or more      |
| kyakusitukubun | bin[4]    |         | 0 or 1         |

## StaticHorseInfoLoader

| name     | type  | unit | range     |
|----------|-------|------|-----------|
| liveyear | float | year | 0 or more |

## RatingLoader

| name               | type  | unit | range     | default |
|--------------------|-------|------|-----------|---------|
| rating_shiba       | float |      | 0 or more | 1400    |
| elapsed_year_shiba | float |      | 0 or more | 0       |
| rating_dirt        | float |      | 0 or more | 1400    |
| elapsed_year_dirt  | float |      | 0 or more | 0       |
| rating_syogai      | float |      | 0 or more | 1400    |
| elapsed_year_syogai       | float |      | 0 or more | 0       |

## StatisticsLoader

| name             | type  | unit | range     |
|------------------|-------|------|-----------|
| ruikeihonshiba   | float | year | 0 or more |
| ruikeifukashiba  | float | year | 0 or more |
| ruikeihondirt    | float | year | 0 or more |
| ruikeifukadirt   | float | year | 0 or more |
| ruikeihonsyogai  | float | year | 0 or more |
| ruikeifukasyogai | float | year | 0 or more |
| ...              | ...   | ...  | ...       |

