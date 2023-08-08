import pandas as pd
import random
import datetime as dt
import streamlit as st
import altair as alt
from pymongo import *
import matplotlib.pyplot as plt

from datetime import datetime, timedelta

def generate_random_dates(num_dates):
    dates = []
    for _ in range(num_dates):
        random_year = random.randint(2000, 2023)
        random_month = random.randint(1, 12)
        random_day = random.randint(1, 28)  # Limit day to 28 to avoid invalid dates for February
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        random_date = datetime(random_year, random_month, random_day, random_hour, random_minute, random_second)
        dates.append(random_date)

    return dates


def get_articles(articles_limit):
    connection = "mongodb://bouman:80um4N!@ec2-15-188-255-64.eu-west-3.compute.amazonaws.com:27017/"
    client = MongoClient(connection)
    db = client.get_database ('bouman_datatank')
    col = db["articles"]
    # query = {
    #     "$and": [
    #         {"language": {"$exists": False}},
    #         {"text": {"$exists": True, "$ne": ""}}
    #     ]
    #     }
    news = col.find({},{"text":0,"title":0,"lemmatized_words":0,"date":0}).limit(articles_limit)
    df = pd.DataFrame(data=news)
    return df 


def create_df(language,newspaper):
    #200 articles
    polarities= [((random.randint(0,200)-100)/100) for x in range(200)]
    languages_ref = ['fr', 'nl']
    languages = [random.sample(languages_ref, 1)[0] for x in range(200)]
    sources_ref = ["lesoir", "dhnet", "rtbf"]
    sources = [random.sample(sources_ref, 1)[0] for x in range(200)]
    dates = generate_random_dates(200)

    polarities_df = pd.DataFrame({"polarity": polarities,"language": languages,"newspaper":sources,"date":dates})
    # print(polarities_df)

    df = get_articles(200)
    
    polarities_df['article_id'] = range(1, len(polarities_df) + 1)
    df['article_id'] = range(1, len(df) + 1)
    df = pd.merge(df, polarities_df, on='article_id')
        
    if language != "All":
        df = df[df['language'] == language]

    if newspaper and "All" not in newspaper:
        df = df[df['newspaper'].isin(newspaper)]
    # print(df.date.dt.year.unique())
    # print(df.groupby(df.date.dt.month)['polarity'].mean())
    # print(df.head(20))
    
    return df

# df = create_df()
# print(df.tail(10))

st.title('DataTank Capstone Project – Sentiment Analysis')


language = st.selectbox("Select Language", ["All", "fr", "nl"])
newspaper = st.multiselect("Select Source", ["lesoir", "dhnet", "rtbf"])

source = create_df(language,newspaper)


# chart = alt.Chart(source).mark_circle().encode(
#     x='date',
#     y='polarity',
#     color='newspaper',
# ).interactive()

# tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

# with tab1:
#     st.altair_chart(chart, theme="streamlit", use_container_width=True)
# with tab2:
#     st.altair_chart(chart, theme=None, use_container_width=True)


chart = (
    alt.Chart(source)
    .mark_line()
    .encode(
        x="date",
        y='polarity',
        color='newspaper'
    )
    .interactive()
)

st.altair_chart(chart, theme="streamlit", use_container_width=True)


st.title('DataTank Capstone Project – Sentiment Analysis')
df = create_df(language,newspaper)



df['polarity_change'] = df['polarity'].diff()

change_chart = (
    alt.Chart(df)
    .mark_area()
    .encode(
        x="date:T",
        y='polarity_change:Q',
    )
    .interactive()
)

st.altair_chart(change_chart, theme="streamlit", use_container_width=True)

