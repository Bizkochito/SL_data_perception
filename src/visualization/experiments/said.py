import pandas as pd
import random
import datetime
import streamlit as st
import altair as alt

def random_date(start, end):
  return (start + datetime.timedelta(
      seconds=random.randint(0, int((end - start).total_seconds())))).isoformat()

def create_df(language, newspaper):
    headers = ["polarity", "source", "date", "title", "text", "language"]
    #200 articles
    polarities= [((random.randint(0,200)-100)/100) for x in range(200)]
    sources_ref = ["lesoir", "standaard", "rtbf"]
    sources = [random.sample(sources_ref, 1)[0] for x in range(200)]
    dates = [random_date(datetime.datetime(2010, 1, 1), datetime.datetime(2021, 1, 12)) for x in range(200)]
    languages_ref = ['fr', 'nl']
    languages = [random.sample(languages_ref, 1)[0] for x in range(200)]

    df = pd.DataFrame({"polarity": polarities, "newspaper": sources, "date": dates, "language": languages})

    if language != "All":
        df = df[df['language'] == language]

    if newspaper and "All" not in newspaper:
        df = df[df['newspaper'].isin(newspaper)]

    return df


st.title('DataTank Capstone Project – Sentiment Analysis')


language = st.selectbox("Select Language", ["All", "fr", "nl"])
newspaper = st.multiselect("Select Source", ["lesoir", "standaard", "rtbf"])

source = create_df(language,newspaper)

source['date'] = pd.to_datetime(source['date'])
source['month'] = source['date'].dt.to_period('M')
average_polarity_by_month = source.groupby('month')['polarity'].mean()


chart = (
    alt.Chart(source)
    .mark_area()
    .encode(
        x=alt.X('date:T', axis=alt.Axis(title='Date')),
        y='polarity',
        color='newspaper'
    )
    .interactive()
)

st.altair_chart(chart, theme="streamlit", use_container_width=True)

average_chart = (
    alt.Chart(average_polarity_by_month.reset_index())
    .mark_line()
    .encode(
        x=alt.X('month:T', axis=alt.Axis(title='Month')),
        y=alt.Y('polarity:Q', axis=alt.Axis(title='Average Polarity')),
        tooltip=['month:T', 'polarity:Q']
    )
    .interactive()
)

st.altair_chart(average_chart, theme="streamlit", use_container_width=True)

show_change = st.checkbox("Show Change in Polarity Score")

if show_change:
    source['polarity_change'] = source['polarity'].diff()
    change_chart = (
        alt.Chart(source)
        .mark_area()
        .encode(
            x="date:T",
            y='polarity_change:Q',
            color='newspaper'
        )
        .interactive()
    )
    
    st.altair_chart(change_chart, theme="streamlit", use_container_width=True)
