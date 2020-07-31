#%% [markdown]
## Project Name: covid_misinformation
### Program Name: CoronaV_Plots.py
### Purpose: To create plots for the presentation. 
##### Date Created: Apr 8th 2020
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
import numpy as np
import math
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

#%% [markdown]
### Create a color scheme
orcl3=cl.scales['3']['seq']['Oranges']
grcl3=cl.scales['3']['seq']['Greys']
bgcl="#111"
linecl=grcl3[0]
fontcl="#eee"
markercl="#e7ad52"

# Fonts
plotly_fonts=["Arial, sans-serif", "Balto, sans-serif", "Courier New, monospace",
            "Droid Sans, sans-serif", "Droid Serif, serif",
            "Droid Sans Mono, sans-serif",
            "Gravitas One, cursive", "Old Standard TT, serif",
            "Open Sans, sans-serif",
            "PT Sans Narrow, sans-serif", "Raleway, sans-serif",
            "Times New Roman, Times, serif"]
plotfont=plotly_fonts[8]
#%%  [markdown]
### Load data
csv_names=[
    "time_series_covid19_confirmed_global",
    "time_series_covid19_deaths_global",
    "time_series_covid19_recovered_global",
    "time_series_covid19_confirmed_US",
    "time_series_covid19_deaths_US",
    ]
rawdf=list(map(lambda x: pd.read_csv(os.path.join(APP_PATH, 'data/TimeSeries/'+x+'.csv')),csv_names))
#%% [markdown]
## ----- Global Confirmed Cases Across Time -----
### Create a list of dates
init_date=datetime.date(2020,1,22)
today=datetime.date(2020,6,30)
dates_real=[init_date] #list of dates as datetime object
dates=['1/22/20'] #list of dates to extract variables 
dates_short=['Jan22']
cur_date=init_date
while cur_date<today: 
    cur_date=cur_date+datetime.timedelta(days=1)
    dates_real.append(cur_date)
    x=dt.strftime(cur_date,'%m/%e/%y')
    y=dt.strftime(cur_date,'%b%d')
    if x.startswith('0'):
        x=x[1:]
    dates.append(x.replace(' ',''))
    dates_short.append(y)
del cur_date,x,y
# Specify how large the bubble should be
bubble_size_index=7
# Create the baseline dataset for world bubble map
last_date=dates[len(dates)-1]
bubble0=rawdf[0][['Province/State','Country/Region', 'Lat', 'Long']]
bubble0=bubble0.assign(Location=np.where(bubble0['Province/State'].isnull(), bubble0['Country/Region'],\
    bubble0['Country/Region']+'-'+bubble0['Province/State']))
bubble0=bubble0.assign(Confirmed=rawdf[0][last_date])
bubble0=bubble0.assign(Deaths=rawdf[1][last_date])
bubble0=bubble0.assign(Recovered=rawdf[2][last_date])
bubble0=bubble0.assign(conf=bubble0['Confirmed'].apply(lambda x: (math.log10(x+1))*bubble_size_index if x>0 else 0))
# Create the baseline dataset for US bubble map on Jan 22
bubble_us0=rawdf[4][['Province_State','Country_Region', 'Admin2','Combined_Key','Population','Lat', 'Long_']]
bubble_us0=bubble_us0.assign(Confirmed=rawdf[3][last_date])
bubble_us0=bubble_us0.assign(Deaths=rawdf[4][last_date])
bubble_us0=bubble_us0.assign(conf=bubble_us0['Confirmed'].apply(lambda x: (math.log10(x+1))*bubble_size_index if x>0 else 0))
### Create the animated map of global confirmed cases
rawdf0=rawdf[0]
lookup=pd.read_csv(os.path.join(APP_PATH,'data','archive_data','UID.csv'))
iso3=lookup[['iso3','Province_State','Country_Region']]
iso3.columns=['iso3','Province/State', 'Country/Region']
confirmed=pd.DataFrame()
for i in range(len(dates)):
    date=dates[i]
    dat=rawdf0[['Province/State', 'Country/Region',date]]
    dat=pd.merge(dat, iso3, how='left', on=['Province/State', 'Country/Region'])
    dat=dat[dat['iso3'].isnull()==0]
    dat=dat[['iso3', 'Country/Region', date]].groupby(['iso3', 'Country/Region']).sum().reset_index()
    dat=dat.assign(conf=dat[date].apply(lambda x: (math.log10(x+1))*bubble_size_index if x>0 else 0))
    dat=dat.assign(date=dates_short[i])
    dat.columns=['iso3','Country','Confirmed','conf','date']
    confirmed=confirmed.append(dat)
del i, dat, date

fig = px.scatter_geo(confirmed, locations="iso3", 
                     hover_name="Country", 
                     text="Confirmed",
                     size="conf",
                     animation_frame="date",
                     projection="natural earth",
                     color_discrete_sequence=[markercl],
                     template="plotly_dark",
                    )
fig.update_layout(
        geo=dict(
            scope="world",
            projection_type="natural earth",
            showland=True,
            landcolor=bgcl,
            showcoastlines=True,
            coastlinecolor=linecl,
            coastlinewidth=0.5,
            showocean=True,
            oceancolor=bgcl,
            showlakes=False,
            showcountries=True,
            countrycolor=linecl,
            countrywidth=0.5,
            bgcolor=bgcl,
        ),
        margin=dict(
            l=0, t=0, b=0, r=0, pad=0),
        paper_bgcolor=bgcl,
        plot_bgcolor=bgcl,
        transition = {'duration': 100}
)
fig.show()
fig.write_html(os.path.join(APP_PATH, 'plots/globalmap_animate.html'))


#%% [markdown]
## ----- Google Trends of Bat Soup Theory -----
searches_bat=[
    'bat soup', 
    'coronavirus bat soup',
    'china bat soup',
    'chinese bat soup',
    'wuhan bat soup',
    'bat soup virus',
]
# Load and process data
result=pd.read_csv(os.path.join(APP_PATH, 'data','GoogleTrends','GT_bat_global_2020-04-26.csv'))
result=result.assign(date=result['date'].apply(lambda x: dt.strptime(x, '%Y-%m-%d')))
# Plot the Trending Results
traces=[]
for kw in searches_bat:
    dat=result[[kw,'date']]
    dat=dat[dat[kw]>0]
    traces.append(
        go.Scatter(
            x=dat['date'],
            y=dat[kw],
            name=kw,
            mode='lines+markers',
            hovertemplate='%{x}'+'<br>'+'Search Interest:%{y}',  
        )
    )
layout = dict(
    paper_bgcolor=bgcl,
    plot_bgcolor=bgcl,
    margin=dict(t=15, r=1, b=0, l=1, pad=0,),
    yaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Search Interest',
    ),
    xaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Date',
    ),
    font=dict(
        family=plotfont,
        size=16,
        color=fontcl
    ),
    legend_orientation='h',
    legend=dict(
        x=0,
        y=-0.2,
    ),
)
fig = go.Figure(data=traces, layout=layout)
fig.write_html(os.path.join(APP_PATH, 'plots','GT_bat_global.html'))

# Add annotation
fig.add_annotation(
            x=datetime.date(2020,1,23),
            y=0,
            text="Chen Qiushi Twitter",
            )
fig.add_annotation(
            x=datetime.date(2020,1,24),
            y=42,
            text="Daily Mail/RT stories",
            )
fig.add_annotation(
            x=datetime.date(2020,1,25),
            y=94,
            text="Paul Joseph Watson Youtube post",
            )
fig.add_annotation(
            x=datetime.date(2020,3,2),
            y=15,
            text="Jesse Watters demanded apologies",
            )
fig.add_annotation(
            x=datetime.date(2020,3,15),
            y=42,
            text="Kodama Boy wrote a song",
            )
fig.update_annotations(
    dict(
            xref="x",
            yref="y",
            showarrow=True,
            arrowcolor=fontcl,
            arrowhead=1,
            arrowside='end',
            ax=45,
            ay=-45,
            font=dict(
                size=12,
                color=fontcl
            ),
))
fig.write_html(os.path.join(APP_PATH, 'plots','GT_bat_global_annotated.html'))

#%% [markdown]
## ----- Google Trends of Wuhan Lab Theory -----
searches_wuhanlab=[
'wuhan virus lab',
'wuhan lab corona virus',
'virus lab in wuhan',
'wuhan bio lab',
'wuhan virology lab',
'wuhan p4 lab',
]
# Load and process data
result=pd.read_csv(os.path.join(APP_PATH, 'data','GoogleTrends','GT_wuhanlab_global_2020-05-04.csv'))
result=result.assign(date=result['date'].apply(lambda x: dt.strptime(x, '%Y-%m-%d')))

# Plot the Trending Results Till end of March 
traces=[]
for kw in searches_wuhanlab:
    dat=result[[kw,'date']]
    dat=dat[dat[kw]>0]
    dat=dat[dat['date']<=date(2020,3,31)]
    traces.append(
        go.Scatter(
            x=dat['date'],
            y=dat[kw],
            name=kw,
            mode='lines+markers',
            hovertemplate='%{x}'+'<br>'+'Search Interest:%{y}',  
        )
    )
layout = dict(
    paper_bgcolor=bgcl,
    plot_bgcolor=bgcl,
    margin=dict(t=15, r=1, b=0, l=1, pad=0,),
    yaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Search Interest',
    ),
    xaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Date',
    ),
    font=dict(
        family=plotfont,
        size=16,
        color=fontcl
    ),
    legend_orientation='h',
    legend=dict(
        x=0,
        y=-0.2,
    ),
)
fig = go.Figure(data=traces, layout=layout)
fig.show()
fig.write_html(os.path.join(APP_PATH, 'plots','GT_wuhanlab_tillMar_20200505.html'))

# Plot the Trending Results Till end of April
traces=[]
for kw in searches_wuhanlab:
    dat=result[[kw,'date']]
    dat=dat[dat[kw]>0]
    dat=dat[dat['date']<=date(2020,4,29)]
    traces.append(
        go.Scatter(
            x=dat['date'],
            y=dat[kw],
            name=kw,
            mode='lines+markers',
            hovertemplate='%{x}'+'<br>'+'Search Interest:%{y}',  
        )
    )
layout = dict(
    paper_bgcolor=bgcl,
    plot_bgcolor=bgcl,
    margin=dict(t=15, r=1, b=0, l=1, pad=0,),
    yaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Search Interest',
    ),
    xaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Date',
    ),
    font=dict(
        family=plotfont,
        size=16,
        color=fontcl
    ),
    legend_orientation='h',
    legend=dict(
        x=0,
        y=-0.2,
    ),
)
fig = go.Figure(data=traces, layout=layout)
fig.show()
fig.write_html(os.path.join(APP_PATH, 'plots','GT_wuhanlab_20200504.html'))

## Zoom in to Jan 24th - 30th
# Create an animated map
result=pd.read_csv(os.path.join(APP_PATH, 'data','GoogleTrends','GT_wuhanlab_US_States_Jan24-30.csv'))
states=pd.read_csv(os.path.join(APP_PATH,'data','states.csv'))
result=pd.merge(result, states, how='left', left_on='State',right_on='State')
searches_wuhanlab=[
'wuhan virus lab',
'wuhan lab corona virus',
'virus lab in wuhan',
'wuhan bio lab',
'wuhan virology lab',
'wuhan p4 lab',
'avg'
]
for trend in searches_wuhanlab:
    fig = px.choropleth(result[['date','State','Abbreviation',trend]], 
                        locations="Abbreviation", 
                        locationmode='USA-states',
                        hover_name="State", 
                        color=trend,
                        animation_frame="date",
                        #projection="natural earth",
                        scope="usa",
                        color_continuous_scale=[bgcl,markercl],
                        template="plotly_dark",
                        )
    fig.update_layout(
            geo=dict(
                scope="usa",
                #projection_type="natural earth",
                showland=True,
                landcolor=bgcl,
                showcoastlines=True,
                coastlinecolor=linecl,
                coastlinewidth=0.5,
                showocean=True,
                oceancolor=bgcl,
                showlakes=False,
                showcountries=True,
                countrycolor=linecl,
                countrywidth=0.5,
                bgcolor=bgcl,
            ),
            margin=dict(
                l=0, t=30, b=0, r=0, pad=0),
            paper_bgcolor=bgcl,
            plot_bgcolor=bgcl,
            title='Search Interest: '+trend,
    )
    fig.show()
    fig.write_html(os.path.join(APP_PATH, 'plots','GT_wuhanlab_US_States_Jan['+trend+'].html'))


## Plotting average of search interset from repeated sampling on Jan 25th, 26th, 27th
for i in ['25','26','27']:
    result=pd.read_csv(os.path.join(APP_PATH, 'data','GoogleTrends','GT_wuhanlab_bootstrap',
    'jan'+i+'_avg.csv'))
    states=pd.read_csv(os.path.join(APP_PATH,'data','states.csv'))
    result=pd.merge(result, states, how='left', left_on='State',right_on='State')
    fig = px.choropleth(result[['State','Abbreviation','avg']], 
                        locations="Abbreviation", 
                        locationmode='USA-states',
                        hover_name="State", 
                        color='avg',
                        scope="usa",
                        color_continuous_scale=[bgcl,markercl],
                        template="plotly_dark",
                        )
    fig.update_layout(
            geo=dict(
                scope="usa",
                showland=True,
                landcolor=bgcl,
                showcoastlines=True,
                coastlinecolor=linecl,
                coastlinewidth=0.5,
                showocean=True,
                oceancolor=bgcl,
                showlakes=False,
                showcountries=True,
                countrycolor=linecl,
                countrywidth=0.5,
                bgcolor=bgcl,
            ),
            margin=dict(
                l=0, t=30, b=0, r=0, pad=0),
            paper_bgcolor=bgcl,
            plot_bgcolor=bgcl,
            title='Average Search Interest',
    )
    fig.show()
    fig.write_html(os.path.join(APP_PATH, 'plots','Avg_wuhanlab_US_States_Jan'+i+'.html'))
#%% [markdown]
## ----- Google Trends of Wuhan Lab Theory -----
searches_5G=[
'5g network',
'5g coronavirus', '5g is coronavirus', '5g coronavirus conspiracy', 
'5g network radiation', '5g towers near me', 
'side effects of 5g network','5g network dangerous',
]
# 5G-Plot 1
result=pd.read_csv(os.path.join(APP_PATH, 'data','GoogleTrends','GT_5G_2019_2020-04-21.csv'))
result=result.assign(date=result['date'].apply(lambda x: dt.strptime(x, '%m/%d/%Y')))
result=result[result['date']<='12/31/2019']
# Plot the Trending Results
traces=[]
for kw in ['5g network','5g network radiation','5g towers near me','side effects of 5g network','5g network dangerous']:
    dat=result[[kw,'date']]
    dat=dat[dat[kw]>0]
    traces.append(
        go.Scatter(
            x=dat['date'],
            y=dat[kw],
            name=kw,
            mode='lines+markers',
            hovertemplate='%{x}'+'<br>'+'Search Interest:%{y}',  
        )
    )
layout = dict(
    paper_bgcolor=bgcl,
    plot_bgcolor=bgcl,
    margin=dict(t=15, r=1, b=0, l=1, pad=0,),
    yaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Search Interest',
    ),
    xaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Date',
    ),
    font=dict(
        family=plotfont,
        size=16,
        color=fontcl
    )
)
fig = go.Figure(data=traces, layout=layout)
fig.show()
fig.write_html(os.path.join(APP_PATH, 'plots','GT_5G_2020_01.html'))
#%% [markdown]
tweets_5g=pd.DataFrame(
    {
        'date':[date(2020,3,24),date(2020,4,2),date(2020,4,2),date(2020,4,3),date(2020,4,6),date(2020,4,7),date(2020,4,8),],
        'y':[15,65,65,100,92,84,100,],
        'name':['M.I.A','Jason Gardiner','Lucy Watson','Wiz Khalifa','Amir Khan','John Cusack','Teddy Riley'],
        'followers_raw':[647975,148831,836124,36349386,2159197,1640347,78807],
        'followers_text':['647.9k','148.8k','836.1k','36.3m','2.1m','1.6m','78.8k']
    }
)
tweets_5g=tweets_5g.assign(followers=tweets_5g['followers_raw'].apply(lambda x: (math.log10(x+1))*9 if x>0 else 0))
tweets_5g['Tweets']=tweets_5g['name']+"("+tweets_5g['followers_text']+" followers)"

# 5G-Plot 2
result=pd.read_csv(os.path.join(APP_PATH, 'data','GoogleTrends','GT_5G_2020daily_2020-04-21.csv'))
result=result.assign(date=result['date'].apply(lambda x: dt.strptime(x, '%m/%d/%Y')))
# Plot the Trending Results
traces=[]
for kw in ['5g network','5g network radiation','5g towers near me','side effects of 5g network','5g network dangerous']:
    dat=result[[kw,'date']]
    dat=dat[dat[kw]>0]
    traces.append(
        go.Scatter(
            x=dat['date'],
            y=dat[kw],
            name=kw,
            mode='lines+markers',
            hovertemplate='%{x}'+'<br>'+'Search Interest:%{y}',  
        )
    )
layout = dict(
    paper_bgcolor=bgcl,
    plot_bgcolor=bgcl,
    margin=dict(t=15, r=1, b=0, l=1, pad=0,),
    yaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Search Interest',
    ),
    xaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Date',
    ),
    font=dict(
        family=plotfont,
        size=16,
        color=fontcl
    )
)
fig = go.Figure(data=traces, layout=layout)
fig.show()
fig.write_html(os.path.join(APP_PATH, 'plots','GT_5G_2020_02.html'))

# 5G- Plot 3
result=pd.read_csv(os.path.join(APP_PATH, 'data','GoogleTrends','GT_5G_2020daily_2020-04-21.csv'))
result=result.assign(date=result['date'].apply(lambda x: dt.strptime(x, '%m/%d/%Y')))
# Plot the Trending Results
traces=[]
for kw in searches_5G:
    dat=result[[kw,'date']]
    dat=dat[dat[kw]>0]
    traces.append(
        go.Scatter(
            x=dat['date'],
            y=dat[kw],
            name=kw,
            mode='lines+markers',
            hovertemplate='%{x}'+'<br>'+'Search Interest:%{y}',  
        )
    )
layout = dict(
    paper_bgcolor=bgcl,
    plot_bgcolor=bgcl,
    margin=dict(t=15, r=1, b=0, l=1, pad=0,),
    yaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Search Interest',
    ),
    xaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Date',
    ),
    font=dict(
        family=plotfont,
        size=16,
        color=fontcl
    )
)
fig = go.Figure(data=traces, layout=layout)
fig.show()
fig.write_html(os.path.join(APP_PATH, 'plots','GT_5G_2020_03.html'))

# 5G- Plot 4
result=pd.read_csv(os.path.join(APP_PATH, 'data','GoogleTrends','GT_5G_2020daily_2020-04-21.csv'))
result=result.assign(date=result['date'].apply(lambda x: dt.strptime(x, '%m/%d/%Y')))
# Plot the Trending Results
traces=[]
for kw in searches_5G:
    dat=result[[kw,'date']]
    dat=dat[dat[kw]>0]
    traces.append(
        go.Scatter(
            x=dat['date'],
            y=dat[kw],
            name=kw,
            mode='lines+markers',
            hovertemplate='%{x}'+'<br>'+'Search Interest:%{y}',  
        )
    )
bubbles=go.Scatter(
    x=tweets_5g['date'],
    y=tweets_5g['y'],
    text=tweets_5g['Tweets'],
    name='Tweets',
    mode='markers',
    marker=dict(
        color=markercl,
        size=tweets_5g['followers'],
    ),
    opacity=0.3,
    hovertemplate='%{x}'+'<br>'+'%{text}',
)
traces.append(bubbles)
layout = dict(
    paper_bgcolor=bgcl,
    plot_bgcolor=bgcl,
    margin=dict(t=15, r=1, b=0, l=1, pad=0,),
    yaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Search Interest',
        tickvals=[0,20,40,60,80,100],
    ),
    xaxis = dict(
        zeroline = False,
        color=linecl,
        showgrid=False,
        title='Date',
        range=[date(2020,3,20),date(2020,4,12)],
    ),
    font=dict(
        family=plotfont,
        size=16,
        color=fontcl
    )
)
fig = go.Figure(data=traces, layout=layout)
fig.add_annotation(
            x=datetime.date(2020,4,3),
            y=100,
            text="'Corona?5g?orBoth?' -- Wiz Khalifa",
            )
fig.update_annotations(
    dict(
            xref="x",
            yref="y",
            showarrow=True,
            arrowcolor=fontcl,
            arrowhead=1,
            arrowside='end',
            ax=-45,
            ay=-30,
            font=dict(
                size=12,
                color=fontcl
            ),
))
fig.show()
fig.write_html(os.path.join(APP_PATH, 'plots','GT_5G_2020_04.html'))