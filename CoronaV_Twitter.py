#%% [markdown]
## Project Name: covid_misinformation
### Program Name: CoronaV_Twitter.py
### Purpose: To download twitter data related to coronavirus. 
##### Date Created: May 6th 2020
#### 
# Twint Documentation:https://github.com/twintproject/twint
#%%
from IPython import get_ipython
get_ipython().magic('reset -sf')
import twint

c=twint.Config()
c.Search = "5G"
c.Lang='en'
c.Since="2020-04-01 00:00:00"
c.Until="2020-04-02 00:00:00"
c.Filter_retweets = True
c.Store_csv = True
c.Output='5g_twitter_2020_04_01.csv'
c.Count=True
twint.run.Search(c)
