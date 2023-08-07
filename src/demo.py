import pandas as pd
import random
import datetime
import streamlit as st
import altair as alt

def random_date(start, end):
  return (start + datetime.timedelta(
      seconds=random.randint(0, int((end - start).total_seconds())))).isoformat()

def create_df():
    headers = ["polarity", "source", "date", "title", "text", "language"]
    #200 articles
    polarities= [((random.randint(0,200)-100)/100) for x in range(200)]
    sources_ref = ["lesoir", "standaard", "rtbf"]
    sources = [random.sample(sources_ref, 1)[0] for x in range(200)]
    dates = [random_date(datetime.datetime(2010, 1, 1), datetime.datetime(2021, 1, 12)) for x in range(200)]
    languages_ref = ['fr', 'nl']
    languages = [random.sample(languages_ref, 1)[0] for x in range(200)]

    return pd.DataFrame({"polarity": polarities, "source": sources, "date": dates, "language": languages})


source = create_df()

chart = alt.Chart(source).mark_circle().encode(
    x='date',
    y='polarity',
    color='source',
).interactive()

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Altair theme.
    st.altair_chart(chart, theme=None, use_container_width=True)