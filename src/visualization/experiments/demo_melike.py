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
        random_year = random.randint(2020, 2023)
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


def monthly_avg_polarity(df):
    df['month'] = df["date"].dt.to_period("M")
    # print(df["month"].unique())
    monthly_avg = df.groupby('month')['polarity'].mean()
    df['avg_polarity'] = df['month'].map(monthly_avg)
    
    return df


language = st.selectbox("Select Language", ["All", "fr", "nl"])
newspaper = st.multiselect("Select Source", ["lesoir", "dhnet", "rtbf"])

df = create_df(language, newspaper)
df_with_avg = monthly_avg_polarity(df)



st.title('TESSSSTTTOOOO')


chart = (
    alt.Chart(df_with_avg)
    .mark_circle()
    .encode(
        x="date",
        y='avg_polarity',
        color='newspaper'
    )
    .interactive()
)

st.altair_chart(chart, theme="streamlit", use_container_width=True)



st.title('TESTOOO2')

df = create_df(language,newspaper)


change_chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x= 'yearmonth(date)',
        y='polarity',
    )
    .interactive()
)

st.altair_chart(change_chart, theme="streamlit", use_container_width=True)


# st.title('TESTOOO3')


# def get_chart(data):
#     # hover = alt.selection_point(
#     #     fields=["month"],
#     #     nearest=True,
#     #     on="mouseover",
#     #     empty=True,
#     # )
#     lines = (
#         alt.Chart(data)
#         .mark_line()
#         .encode(
#             x="yearmonth(date):T",
#             y="avg_polarity",
#             color="newspaper",
#         )
#     )

#     # Draw points on the line, and highlight based on selection
#     points = lines.transform_filter(hover).mark_circle(size=65)

#     # Draw a rule at the location of the selection
#     tooltips = (
#         alt.Chart(data)
#         .mark_rule()
#         .encode(
#             x="yearmonth(date)",
#             y="polarity",
#             opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
#             tooltip=[
#                 alt.Tooltip("date", title="Date"),
#                 alt.Tooltip("polarity", title="poloo"),
#             ],
#         )
#         .add_params(hover)
#     )
#     return (lines + points + tooltips).interactive()

# chart = get_chart(df_with_avg[df_with_avg["month"]])
# st.altair_chart(chart, theme="streamlit", use_container_width=True)