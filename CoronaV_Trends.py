#%% [markdown]
## Project Name: covid_misinformation
### Program Name: CoronaV_Trends.py
### Purpose: To download google trends data related to coronavirus. 
##### Date Created: Apr 8th 2020
#### 
# Pytrends Documentation:https://github.com/GeneralMills/pytrends
#%% [markdown]
from IPython import get_ipython
get_ipython().magic('reset -sf')
import datetime
from datetime import datetime as dt
from datetime import date
import os 
import pathlib
import colorlover as cl
import plotly.graph_objs as go
import chart_studio.plotly as py
import plotly.express as px
import pandas as pd
from pytrends.request import TrendReq
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

pytrends = TrendReq(hl='en-US', tz=360, retries=2, backoff_factor=0.1)
#%% [markdown]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Bat soup theory~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
today=datetime.date(2020,4,26)
search_time='2020-01-01 '+str(today)
searches_bat=[
    'bat soup', 
    'coronavirus bat soup',
    'china bat soup',
    'chinese bat soup',
    'wuhan bat soup',
    'bat soup virus',
]
groupkeywords = list(zip(*[iter(searches_bat)]*1))
groupkeywords = [list(x) for x in groupkeywords]
# Download search interest of bat key words
dicti = {}
i = 1
for trending in groupkeywords:
    pytrends.build_payload(
        trending, 
        timeframe = search_time,
    )
    dicti[i] = pytrends.interest_over_time()
    i+=1
result = pd.concat(dicti, axis=1)
result.columns = result.columns.droplevel(0)
result = result.drop('isPartial', axis = 1)
#result['date']=result.index.date
result.to_csv(os.path.join(APP_PATH, 'data', 'GoogleTrends','GT_bat_global_'+str(today)+'.csv'), header=True)


#%% [markdown]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Wuhan Lab theory~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
today=datetime.date(2020,5,4)
search_time='2020-01-01 '+str(today)
searches_wuhanlab=[
'wuhan virus lab',
'wuhan lab corona virus',
'virus lab in wuhan',
'wuhan bio lab',
'wuhan virology lab',
'wuhan p4 lab',
'wuhan level 4 lab',
'wuhan bsl-4 lab',
]
groupkeywords = list(zip(*[iter(searches_wuhanlab)]*1))
groupkeywords = [list(x) for x in groupkeywords]
#%% [markdown]
# Download search interest of wuhanlab key words 
dicti = {}
i = 1
for trending in groupkeywords:
    pytrends.build_payload(
        trending, 
        timeframe = search_time,
    )
    dicti[i] = pytrends.interest_over_time()
    i+=1
result = pd.concat(dicti, axis=1)
result.columns = result.columns.droplevel(0)
result = result.drop('isPartial', axis = 1)
result.to_csv(os.path.join(APP_PATH, 'data', 'GoogleTrends','GT_wuhanlab_global_'+str(today)+'.csv'), header=True)
#%% [markdown]
# Select one week Jan 24th - Jan 30th to downolad google trend by state
search_times=[
 '2020-01-24 2020-01-24',
 '2020-01-25 2020-01-25',
 '2020-01-26 2020-01-26',
 '2020-01-27 2020-01-27',
 '2020-01-28 2020-01-28',
 '2020-01-29 2020-01-29'
]

#search_times=[
#    '2020-04-14 2020-4-14',
#    '2020-04-15 2020-4-15',
#    '2020-04-16 2020-4-16',
#    '2020-04-17 2020-4-17',
#    '2020-04-18 2020-4-18',
#    '2020-04-19 2020-4-19',
#]
#%% [markdown]
j=1
for trending in groupkeywords:
    dicti = {}
    i = 1
    for d in search_times:
        pytrends.build_payload(trending, geo='US', timeframe=d)
        dicti[i]=pytrends.interest_by_region( inc_low_vol=True, inc_geo_code=False)
        dicti[i]['date']=search_times[i-1][:10]
        i+=1
    if j==1:
        result = pd.concat(dicti, axis=0)
        result = result.reset_index()
        result = result.drop(['level_0'], axis=1)   
    else: 
        x=pd.concat(dicti, axis=0)
        x=x.reset_index().drop(['level_0', 'geoName','date'], axis=1)
        result=pd.concat([result,x], axis=1)        
    j+=1
del x,i,j,d
#%% [markdown]
result.columns=['State', 'wuhan virus lab', 'date',
 'wuhan lab corona virus',
 'virus lab in wuhan',
 'wuhan bio lab',
 'wuhan virology lab',
 'wuhan p4 lab',
 'wuhan level 4 lab',
 'wuhan bsl-4 lab']
result=result[['date','State', 'wuhan virus lab', 'wuhan lab corona virus',
 'virus lab in wuhan', 'wuhan bio lab', 'wuhan virology lab',
 'wuhan p4 lab', 'wuhan level 4 lab', 'wuhan bsl-4 lab']]
result.to_csv(os.path.join(APP_PATH, 'data', 'GoogleTrends','GT_wuhanlab_US_States_Jan24-30.csv'), header=True)
#%% [markdown]
# Sampling search interest on Jan 25th, 26th, 27th
# Repeat this section of code as needed for repeat sampling
# First reset timezone to PST
pytrends = TrendReq(hl='en-US', tz=480, timeout=(10,25), retries=2, backoff_factor=0.1)
search_times=[
    '2020-01-25 2020-01-25', '2020-01-26 2020-01-26', '2020-01-27 2020-01-27',
]
j=1
for trending in groupkeywords:
    dicti = {}
    i = 1
    for d in search_times:
        pytrends.build_payload(
            trending, 
            geo='US', 
            timeframe=d)
        dicti[i]=pytrends.interest_by_region(inc_low_vol=True, inc_geo_code=False)
        dicti[i]['date']=search_times[i-1]
        i+=1
    if j==1:
        result = pd.concat(dicti, axis=0)
        result = result.reset_index()
        result = result.drop(['level_0'], axis=1)   
    else: 
        x=pd.concat(dicti, axis=0)
        x=x.reset_index().drop(['level_0', 'geoName','date'], axis=1)
        result=pd.concat([result,x], axis=1)        
    j+=1
del x,i,j, d
result.columns=['State', 'wuhan virus lab', 'date',
 'wuhan lab corona virus',
 'virus lab in wuhan',
 'wuhan bio lab',
 'wuhan virology lab',
 'wuhan p4 lab',
 'wuhan level 4 lab',
 ]
result=result[['date','State', 'wuhan virus lab', 'wuhan lab corona virus',
 'virus lab in wuhan', 'wuhan bio lab', 'wuhan virology lab',
 'wuhan p4 lab', 'wuhan level 4 lab']]
result['avg']=result[['wuhan virus lab', 'wuhan lab corona virus',
 'virus lab in wuhan', 'wuhan bio lab', 'wuhan virology lab',
 'wuhan p4 lab', 'wuhan level 4 lab']].mean(axis=1)
result=result.assign(date=result['date'].apply(lambda x: x[:10]))
result.reset_index(drop=True, inplace=True)
result.to_csv(os.path.join(APP_PATH, 'data', 'GoogleTrends','GT_wuhanlab_bootstrap','GT_wuhanlab_US_jan25_'+str(today)+'_.csv'), 
header=True, index=False)
#%% [markdown]
# Read in repeat sampling
for i in [25,26,27]: 
    df=pd.DataFrame()
    for filename in [
    'GT_wuhanlab_US_jan25_2020-06-13',
    'GT_wuhanlab_US_jan25_2020-06-25',
    'GT_wuhanlab_US_jan25_2020-06-30_0',
    'GT_wuhanlab_US_jan25_2020-06-30_1',
    'GT_wuhanlab_US_jan25_2020-06-30_2',
    'GT_wuhanlab_US_jan25_2020-07-01_0',
    'GT_wuhanlab_US_jan25_2020-07-01_1',
    'GT_wuhanlab_US_jan25_2020-07-01_2',
    'GT_wuhanlab_US_jan25_2020-07-01_3',
    'GT_wuhanlab_US_jan25_2020-07-01_4',
    'GT_wuhanlab_US_jan25_2020-07-01_5',
    'GT_wuhanlab_US_jan25_2020-07-02_0',    
    'GT_wuhanlab_US_jan25_2020-07-02_1',    
    'GT_wuhanlab_US_jan25_2020-07-02_2',
    'GT_wuhanlab_US_jan25_2020-07-04_0',
    'GT_wuhanlab_US_jan25_2020-07-04_1',
    'GT_wuhanlab_US_jan25_2020-07-06_0',
    'GT_wuhanlab_US_jan25_2020-07-06_1',
    'GT_wuhanlab_US_jan25_2020-07-07_0',
    'GT_wuhanlab_US_jan25_2020-07-07_1',
    ]:
        tmp=pd.read_csv(os.path.join(APP_PATH,'data','GoogleTrends','GT_wuhanlab_bootstrap', filename+'.csv'))
        tmp=tmp[tmp.date=='1/'+str(i)+'/2020'][['date','State','avg']]
        df=pd.concat([df,tmp])
    del filename, tmp
    df2=df.groupby('State').mean()
    df2.to_csv(os.path.join(APP_PATH, 'data', 'GoogleTrends','GT_wuhanlab_bootstrap','jan'+str(i)+'_avg.csv'), header=True)
    del df2, df
del i
#%% [markdown]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5G theory~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
today=datetime.date(2020,4,21)
search_time='2020-01-01 '+str(today)

searches_5G=[
'5g network',
'5g coronavirus', '5g is coronavirus', '5g coronavirus conspiracy', 
'5g network radiation', '5g towers near me', 
'side effects of 5g network','5g network dangerous',
]
groupkeywords = list(zip(*[iter(searches_5G)]*1))
groupkeywords = [list(x) for x in groupkeywords]
dicti = {}
i = 1
for trending in groupkeywords:
    pytrends.build_payload(
        trending, 
        timeframe = search_time,
    )
    dicti[i] = pytrends.interest_over_time()
    i+=1
result = pd.concat(dicti, axis=1)
result.columns = result.columns.droplevel(0)
result = result.drop('isPartial', axis = 1)
result['date']=result.index.date
# Save Results into a csv file
result.to_csv(os.path.join(APP_PATH, 'data', 'GoogleTrends','GT_5G_2019_'+str(today)+'.csv'), header=True)