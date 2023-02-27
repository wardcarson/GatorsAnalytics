import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import snscrape.modules.twitter as sntwitter
import snscrape
import os

# Input Code to run application through TERMINAL
# streamlit run /Users/carsonward/Desktop/scrape/dashboard.py

# *** ACTIVATING VIRTUAL ENVIRONMENT (DO BEFORE RUNNING CODE) ***
# Run : source Desktop/scrape/tiktok/bin/activate
# in terminal to aviate environment this code can run in


# Step 1 : Scrape site for data that we want
# Creating an instance of the Instaloader class
# Step 1 : Scrape site for data that we want
def scrapesite(url):
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
    }
    result = requests.get(url, headers=headers)
    src = result.content
    soup = BeautifulSoup(src)
    acc_data = [ item.get_text(strip=True) for item in soup.find_all(class_="report-header-number") ]
    return acc_data[0]

def scrapesites(ats):
    bank = []
    for at in ats:
        bank.append(scrapesite('https://socialstats.info/report/' + at + '/instagram'))
    return bank


##
## IG FOLLOWERS BY SEC SCHOOL
##

test_ats = ['floridagators','lsusports','ua_athletics','auburntigers','ugaathletics','vol_sports','gamecocksonline','12thman','vucommodores','mizzouathletics','arkrazorbacks','ukathletics','olemissathletics','hailstate']
test = scrapesites(test_ats)

df = pd.DataFrame({'Account': test_ats,
     'Followers': test,
    },index=('UF','LSU','BAMA','AUB','UGA','UT','uSC','A&M','Vandy','MIZ','ARK','UK','UM','MSU'))

df['Followers'] = df['Followers'].str.replace(',','').astype(int)

print(df)

##
## IG FOLLOWERS BY TOP 25 SCHOOLS
##
top25_ats = ['ohiostathletics','goducks','floridagators','texaslonghorns','ugaathletics','ua_athletics','goheels','uwbadgers','ukathletics','huskers','arkrazorbacks','auburntigers','ou_athletics','gamecocksonline','theiowahawkeyes','gocards','usc_athletics','miamihurricanes','msu_athletics','thefightingirish','seminoles','vol_sports','lsusports','kuathletics','clemsontigers']
top25 = scrapesites(top25_ats)

df25 = pd.DataFrame({'Account': top25_ats,
     'Followers': top25,},
      index=('OSU','UO','UF','TEXAS','UGA','BAMA','UNC','UW','UK','NEB','ARK','AUB','OU','uSC','IOWA','UL','USC','UM','MSU','ND','FSU','UT','LSU','KU','UC'))

df25['Followers'] = df25['Followers'].str.replace(',','').astype(int)


# SCRAPES TWITTER FOLLOWERS AND RETURNS
def twitfollowers(ats):
    tweet_count = 1
    data = {}
    # Using OS library to call CLI commands in Python
    for username in ats:
        os.system("snscrape --jsonl --max-results {} twitter-search 'from:{}'> user-tweets.json".format(tweet_count, username))
        tweets_df1 = pd.read_json('user-tweets.json', lines=True)
        temp = tweets_df1['user'][0]
        data[username] = temp['followersCount']
    return data

twit_ats_sec = ['floridagators','ugaathletics','vol_sports','gamecocksonline',
            'ukathletics','mizzouathletics','vucommodores','lsusports','ua_athletics',
            'auburntigers','olemisssports','hailstate','arkrazorbacks','12thman']

twitter_followes_dict_sec = twitfollowers(twit_ats_sec)




gatorlogo = Image.open('floridagatorlogo.png')
dash = Image.open('socdash.png')
# # Initializing Streamlit App
st.image(dash)

# col1, col2 = st.columns(2,gap="small")
# with col1:
#     st.title('Gators Social Dashboard')
# with col2:
#     st.image(gatorlogo,width=200)

col3, col4 = st.columns(2,gap="medium")

with col3:
    st.markdown("[![Foo](https://raw.githubusercontent.com/wardcarson/GatorsAnalytics/main/insta.png)](https://www.instagram.com/floridagators)") 
with col4:
    st.markdown("[![Foo](https://raw.githubusercontent.com/wardcarson/GatorsAnalytics/main/twit.png)](https://www.twitter.com/floridagators)") 


twit_df = pd.DataFrame.from_dict(twitter_followes_dict_sec,orient='index')
twit_df['Account'] = twit_df.index
twit_df.rename(columns={ twit_df.columns[0]: "Followers" }, inplace=True)
twit_df['Followers'] = twit_df['Followers'].astype(int)
twit_df.index = ('UF','UGA','UT','uSC','UK','MIZ','Vandy','LSU','BAMA','AUB','UM','MSU','ARK','A&M')
print(twit_df)

combined_df = pd.merge(df,twit_df,left_index=True,right_index=True)
print(combined_df)

colormap = {
                    "floridagators" : "blue",
                    "lsusports" : "purple",
                    "ua_athletics" : "crimson",
                    "auburntigers" : "navy",
                    "ugaathletics" : "red",
                    "vol_sports" : "orange",
                    "gamecocksonline" : "maroon",
                    "12thman" : "maroon",
                    "vucommodores" : "black",
                    "mizzouathletics" : "gold",
                    "arkrazorbacks" : "crimson",
                    "ukathletics" : "blue",
                    "olemisssports" : "navy",
                    "hailstate" : "maroon"}

fig_comb = px.scatter(combined_df, x='Followers_x', y='Followers_y',text='Account_x',title='Plot of IG vs Twitter Followers for SEC Schools')
fig_comb.update_traces(textposition='top center')
fig_comb.update_layout(xaxis_title= 'IG Followers')
fig_comb.update_layout(yaxis_title= 'Twitter Followers')

fig_twit = px.bar(twit_df, title= 'Twitter Followers by SEC School',y="Followers",x='Account',color="Account",
                color_discrete_map={
                    "floridagators" : "blue",
                    "lsusports" : "purple",
                    "ua_athletics" : "crimson",
                    "auburntigers" : "navy",
                    "ugaathletics" : "red",
                    "vol_sports" : "orange",
                    "gamecocksonline" : "maroon",
                    "12thman" : "maroon",
                    "vucommodores" : "black",
                    "mizzouathletics" : "gold",
                    "arkrazorbacks" : "crimson",
                    "ukathletics" : "blue",
                    "olemisssports" : "navy",
                    "hailstate" : "maroon"}
                    )
fig_twit.update_layout(xaxis={'categoryorder':'total descending'})

fig_twit.update_layout(template="plotly_dark")
fig_twit.update_layout(paper_bgcolor="white")


fig = px.bar(df, x="Account", y="Followers", title="IG Followers by SEC School",color="Account",
                color_discrete_map={
                    "floridagators" : "blue",
                    "lsusports" : "purple",
                    "ua_athletics" : "crimson",
                    "auburntigers" : "navy",
                    "ugaathletics" : "red",
                    "vol_sports" : "orange",
                    "gamecocksonline" : "maroon",
                    "12thman" : "maroon",
                    "vucommodores" : "black",
                    "mizzouathletics" : "gold",
                    "arkrazorbacks" : "crimson",
                    "ukathletics" : "blue",
                    "olemissathletics" : "navy",
                    "hailstate" : "maroon"}
                    )


fig25 = px.bar(df25, x="Account", y="Followers", title="IG Followers by top 25 School",color="Account",
                color_discrete_map={
                    "floridagators" : "blue",
                    "lsusports" : "purple",
                    "ua_athletics" : "crimson",
                    "auburntigers" : "navy",
                    "ugaathletics" : "red",
                    "vol_sports" : "orange",
                    "gamecocksonline" : "maroon",
                    "arkrazorbacks" : "crimson",
                    "ukathletics" : "blue",
                    "ohiostathletics":"red",
                    "goducks":"green",
                    "texaslonghorns":"orange",
                    "goheels":"lightskyblue",
                    "uwbadgers":"red",
                    "huskers":"red",
                    "ou_athletics":"maroon",
                    "theiowahawkeyes":"yellow",
                    "gocards":"red",
                    "usc_athletics":"maroon",
                    "miamihurricanes":"orange",
                    "msu_athletics":"green",
                    "thefightingirish":"navy",
                    "seminoles":"maroon",
                    "kuathletics":"blue",
                    "clemsontigers":"orange",
                    }
                    )
fig25.update_layout(xaxis={'categoryorder':'total descending'})
fig25.update_layout(template="plotly_dark")
fig25.update_layout(paper_bgcolor="white")


sec = Image.open('sec2.png')
fig.update_layout(template="plotly_dark")
fig.update_layout(paper_bgcolor="white")
fig.update_layout(xaxis={'categoryorder':'total descending'})

newnames = {
                    "floridagators" : "Florida",
                    "lsusports" : "LSU",
                    "ua_athletics" : "Alabama",
                    "auburntigers" : "Auburn",
                    "ugaathletics" : "Georgia",
                    "vol_sports" : "Tennessee",
                    "gamecocksonline" : "South Carolina",
                    "12thman" : "Texas A&M",
                    "vucommodores" : "Vanderbilt",
                    "mizzouathletics" : "Missouri",
                    "arkrazorbacks" : "Arkansas",
                    "ukathletics" : "Kentucky",
                    "olemissathletics" : "Ole Miss",
                    "hailstate" : "Mississippi State"}


fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

#st.image(sec,width=200)
fig.add_layout_image(
        dict(
            source=sec,
            xref="paper",
            yref="paper",
            x=1,
            y=1.05,
            sizex= 0.5,
            sizey= 0.5,
            xanchor="right", yanchor="top",
            layer="below",
            opacity=0.6)
)
fig_twit.add_layout_image(
        dict(
            source=sec,
            xref="paper",
            yref="paper",
            x=1,
            y=1.05,
            sizex= 0.5,
            sizey= 0.5,
            xanchor="right", yanchor="top",
            layer="below",
            opacity=0.6)
)


tab1, tab2, tab3 = st.tabs(["Instagram Statistics", "Twitter Statistics", "Combined"])

with tab1:
    st.plotly_chart(fig)
    st.plotly_chart(fig25)

with tab2:
    st.plotly_chart(fig_twit)

with tab3:
    st.plotly_chart(fig_comb)



# [ "blue",
#                  "purple",
#                  "crimson",
#                  "navy",
#                  "red",
#                  "orange",
#                  "maroon",
#                  "burgandy",
#                  "black",
#                  "gold",
#                  "crimson",
#                  "blue",
#                  "navy",
#                  "maroon"]