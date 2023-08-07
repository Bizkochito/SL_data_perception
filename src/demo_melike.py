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
    .mark_area()
    .encode(
        x="date",
        y='polarity',
        color='newspaper'
    )
    .interactive()
)

st.altair_chart(chart, theme="streamlit", use_container_width=True)