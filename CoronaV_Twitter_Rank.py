#%% [markdown]
## Project Name: covid_misinformation
### Program Name: CoronaV_Twitter_Rank.py
### Purpose: To plot the Twitter users mentioned or quoted the most by day 
##### Date Created: June 23rd 2020
#### 
#%%
from IPython import get_ipython
#get_ipython().magic('reset -sf')
import datetime
from datetime import datetime as dt
from datetime import date
import os 
from os import listdir
from os.path import isfile, join
import pathlib
import colorlover as cl
import plotly.graph_objs as go
import chart_studio.plotly as py
import plotly.express as px
import pandas as pd
import numpy as np
import math
import re
import twint
import jgraph as jg
import ast
import functools
import operator
from collections import Counter
import json
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
#%%
t0=dt.now()
print('-------------------------Start Running Code------------------')
print('Time:', t0)
#%% 
# Styles
plotlycl=px.colors.qualitative.Plotly
orcl3=cl.scales['3']['seq']['Oranges']
grcl3=cl.scales['3']['seq']['Greys']
bgcl="#111"
linecl=grcl3[0]
fontcl="#eee"
markercl="#e7ad52"
plotfont="Open Sans, sans-serif"
#%%
# Reading in the Tweets from April 1st to 4th
datafiles=['5g_twitter_2020_04_01.csv', '5g_twitter_2020_04_02.csv', 
            '5g_twitter_2020_04_03.csv', '5g_twitter_2020_04_04.csv',
            '5g_twitter_2020_04_05.csv', '5g_twitter_2020_04_06.csv', 
            '5g_twitter_2020_04_07.csv', 
            '5g_twitter_2020_04_08.csv', 
            ]
dflst=list(
    map(
        lambda x: pd.read_csv(
            os.path.join(APP_PATH, 'data', 'Twitter', x),
            error_bad_lines=False,
            dtype={
                'id': int, 'conversation_id': int, 'created_at': int, 'date': object, 'time': object,
                'timezone': object, 'user_id': int, 'username': str, 'name': str, 'place': str,
                'tweet': str, 'mentions': object, 'urls': object, 'photos': object, 'replies_count': int,
                'retweets_count': int, 'likes_count': int, 'hashtags': str, 'cashtags': str,
                'link': str, 'reweet': bool, 'quote_url': str, 'video': int, 'near': float,
                'geo': float, 'source': float, 'user_rt_id': float, 'user_rt': float, 'retweet_id': float,
                'reply_to': object, 'retweet_date': float, 'translate': float, 'trans_src': float,
                'trans_dest': float,
            }
        ),
        datafiles
        )
    )
df0=pd.concat(dflst)
username_dict=dict(zip(df0.username, df0.name))
del df0
#%%
username_dict['youtube']='YouTube'
username_dict['realdonaldtrump']='Donald J. Trump'
username_dict['drzwelimkhize']='Dr Zweli Mkhize'
username_dict['piersmorgan']='Piers Morgan'
username_dict['borisjohnson']='Boris Johnson #StayAlert'
username_dict['stormisuponus']='Storm Is Upon Us'
username_dict['inevitable_et']='l E T 17'
username_dict['blaackdiamonnd']='theREALBlack💎'
username_dict['realjameswoods']='James Woods'
username_dict['realcandaceo']='Candace Owens'
username_dict['umvrr']='_umvr'
username_dict['holbornlolz']='Old Holborn ✘'
username_dict['x22report']='X22 Report'
username_dict['who']='World Health Organization (WHO)'
username_dict['cjtruth']='CJTRUTH⭐️⭐️⭐️'
username_dict['clarkemicah']='Peter Hitchens'
username_dict['potus']='President Trump'
username_dict['alexbkane']='Alex Kane'
username_dict['billgates']='Bill Gates'
username_dict['amandaholden']='Amanda Holden'
username_dict['drisapantami']='Isa Ali Pantami, PhD'
username_dict['ncdcgov']='NCDC'
username_dict['worldstar']='WORLDSTARHIPHOP'
username_dict['jimalkhalili']='Jim Al-Khalili'
username_dict['pastorchrislive']='Pastor Chris'
username_dict['sam_adeyemi']='Sam Adeyemi'
username_dict['apostlesuleman']='Apst Johnson Suleman'
#%%
def twitter_rank(ind):
    df=pd.read_csv(
            os.path.join(APP_PATH, 'data', 'Twitter', datafiles[ind]),
            error_bad_lines=False,
            dtype={
                'id': int, 'conversation_id': int, 'created_at': int, 'date': object, 'time': object,
                'timezone': object, 'user_id': int, 'username': str, 'name': str, 'place': str,
                'tweet': str, 'mentions': object, 'urls': object, 'photos': object, 'replies_count': int,
                'retweets_count': int, 'likes_count': int, 'hashtags': str, 'cashtags': str,
                'link': str, 'reweet': bool, 'quote_url': str, 'video': int, 'near': float,
                'geo': float, 'source': float, 'user_rt_id': float, 'user_rt': float, 'retweet_id': float,
                'reply_to': object, 'retweet_date': float, 'translate': float, 'trans_src': float,
                'trans_dest': float,
            }
        )
    df=df.drop(['retweet','near','geo','source','user_rt_id','user_rt','retweet_id','retweet_date','translate','trans_src','trans_dest'], axis=1)
    df.drop_duplicates(subset='link', keep='first',inplace=True)
    df.sort_values('retweets_count', inplace=True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    df=df[df.tweet.str.contains('corona|virus|covid', flags=re.IGNORECASE)]
    u_name=list(df['username'])
    quote_url=list(df['quote_url'])
    urls=list(map(lambda x: list(ast.literal_eval(x.lower())), list(df['urls'])))
    reply_to=list(df['reply_to'])
    reply_to_u=list(map(lambda x: list(pd.DataFrame(ast.literal_eval(x.lower()))['username']), reply_to))
    mentions=list(map(lambda x: list(ast.literal_eval(x.lower())), list(df['mentions'])))
    reacts_to=[]
    for i in range(len(mentions)):
        x=[]
        x1=mentions[i]
        x2=reply_to_u[i]
        x3=quote_url[i]
        x4=urls[i]
        x+=x1    
        x+=x2
        if isinstance(x3,str):
            x+=re.findall('twitter.com/([A-Za-z0-9]+)/status/[0-9]+', x3.lower())    
        if len(x4)>0:
            x4b=list(map(lambda x: re.findall('twitter.com/([A-Za-z0-9]+)/status/[0-9]+', x.lower()), x4))
            x4=list(set(functools.reduce(operator.iconcat, x4b,[])))
            x+=x4
        if u_name[i] in x:
            x.remove(u_name[i])
        x=list(set(x))
        reacts_to+=[x]        
    df['source']=reacts_to
    reacts_to2=[]
    for j in range(len(reacts_to)):
        if len(reacts_to[j])>0:
            reacts_to2+=reacts_to[j]
    freq=Counter(reacts_to2)
    return(freq)
freq0=twitter_rank(0)
#%%
freqs=list(map(lambda x: twitter_rank(x), range(len(datafiles))))
#%%
#dates=[datetime.date(2020,4,i) for i in range(1,9)]
dates=['Apr01','Apr02','Apr03','Apr04','Apr05','Apr06','Apr07','Apr08',]
#%%
top_n=20
freq_df=pd.DataFrame(freqs[0].most_common(top_n))
freq_df['date']=dates[0]
for i in range(1,8):
    tmp=pd.DataFrame(freqs[i].most_common(top_n))
    tmp['date']=dates[i]
    freq_df=pd.concat([freq_df, tmp])
del i, tmp
freq_df=freq_df.reset_index(drop=True)
freq_df.columns=['Username', 'Count','Date']
#%%
grp=['bbcnews', 'bbcrealitycheck', 'bbcworld', 'channelstv', 'cnn', 'dcms', 'eorganiser',
 'fmocdenigeria', 'huawei', 'imjustbrum', 'londonrealtv', 'mobilepunch', 'ncdcgov', 'news24',
 'newsdeynigeria', 'nypost', 'pmnewsnigeria', 'rt_com', 'sgtreport', 'skynews', 'thecableng',
 'verge', 'who', 'worldstar', 'x22report', 'youtube']

nigeria=['alphamodella', 'apostlesuleman', 'asemota', 'channelstv', 'daddyfrz', 'dehkunle',
 'dino_melaye', 'drisapantami', 'drjoeabah', 'fmocdenigeria', 'islimfit', 'mobilepunch',
 'ncdcgov', 'newsdeynigeria', 'omojuwa', 'pastorchrislive', 'pmnewsnigeria',  'realffk',
  'sam_adeyemi',  'segalink', 'thecableng',  'umvrr']

uk=['afneil', 'amandaholden', 'bbcnews', 'bbcrealitycheck', 'bbcworld', 'borisjohnson',
 'breesanna', 'carljackmiller', 'charliehtweets', 'chrisbrexitwto', 'clarkemicah', 'davidicke',
 'dcms', 'drolufunmilayo', 'garylineker', 'imjustbrum', 'james40428873', 'jimalkhalili',
 'lady44sassy', 'londonrealtv', 'mrjamesob', 'piersmorgan', 'prisonplanet', 'rhiannonjudithw',
 'skynews',  'walegates']

us=['alexbkane', 'billgates', 'blaackdiamonnd', 'christinepolon1', 'cjtruth', 'cnn', 'inevitable_et',
 'jbouie', 'nypost', 'potus', 'realcandaceo', 'realdonaldtrump', 'realjameswoods', 'sgtreport',
 'stormisuponus', 'tyrone_brother', 'verge',  'wizkhalifa', 'worldstar', 'youtube']

qanon=['christinepolon1', 'cjtruth', 'inevitable_et', 'ipot1776', 'sgtreport', 'stormisuponus', 'x22report']
#%%
freq_df=freq_df[freq_df['Username'].isin(grp)==0]
#%%
freq_df=freq_df.assign(Group=np.where(freq_df['Username'].isin(grp), "Group", "Individual"))
freq_df=freq_df.assign(Country=np.where(freq_df['Username'].isin(nigeria), 'Nigeria', 
                                    np.where(freq_df['Username'].isin(uk), 'UK',
                                    np.where(freq_df['Username'].isin(us), 'USA', 
                                    'Other'))))
freq_df=freq_df.assign(Size=freq_df['Count'].apply(lambda x: (math.log10(x+1))*20 if x>0 else 0))
labels=[]
for x in freq_df['Username']:
    if x.lower() in username_dict:
        labels.append(username_dict[x.lower()])
    else:
        labels.append('NA')
del x
freq_df['Label']=labels
del labels
freq_df['User']=freq_df['Label']+"(@"+freq_df['Username']+")"
#%%
traces=[]
ctr=['USA','UK','Nigeria','Other']
for i in range(len(ctr)):
    d=freq_df[freq_df['Country']==ctr[i]]
    traces.append(
        go.Scatter(
        x=d['Date'], 
        y=d['Count'],
        name=ctr[i],
        mode='markers',
        text=d['User'],
        hovertemplate='%{text}: '+ '%{y}',
        marker=go.scatter.Marker(
            size=d['Size'],
            color=plotlycl[i],
            )
        )
    )
fig=go.Figure(data=traces)
fig.update_layout(
        paper_bgcolor=bgcl,
        plot_bgcolor=bgcl,
        font=dict(
            family=plotfont, size=12,
            color='rgba(255, 255, 255, 0.5)',
        ),
        yaxis=dict(
            zeroline=False,
            title='Count',
            showgrid=False,
            color=grcl3[2],
        ), 
        xaxis=dict(
            zeroline=False,
            title='Date',
            showgrid=False,
            color=grcl3[2],
        ),
        legend=dict(
            x=1,
            y=-0.2,
        ),
)
fig.write_html(os.path.join(APP_PATH, 'plots','twitter_rank_20200624.html'))