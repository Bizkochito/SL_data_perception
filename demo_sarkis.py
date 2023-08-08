import streamlit as st
import numpy as np
import datetime
import altair as alt
from bokeh.plotting import figure
import pandas as pd

def random_date(start, end):
    return (start + datetime.timedelta(
        seconds=np.random.randint(0, int((end - start).total_seconds())))).isoformat()

def create_df():
    polarities = [((np.random.randint(0, 200) - 100) / 100) for _ in range(200)]
    sources_ref = ["lesoir", "standaard", "rtbf"]
    sources = [np.random.choice(sources_ref) for _ in range(200)]
    dates = [random_date(datetime.datetime(2010, 1, 1), datetime.datetime(2021, 1, 12)) for _ in range(200)]
    languages_ref = ['fr', 'nl']
    languages = [np.random.choice(languages_ref) for _ in range(200)]

    return pd.DataFrame({"polarity": polarities, "source": sources, "date": dates, "language": languages})

def media_selection():
    st.title("Media Selection")

    data = create_df()
    
    language = st.selectbox("Select a language:", ['nl', 'fr'])
    selected_source = st.selectbox("Select a source:", data["source"].unique())
    filtered_data = data[(data["source"] == selected_source) & (data["language"] == language)]

    use_slider = st.checkbox("Use Sentiment Slider")
    slider_value = None

    if use_slider:
        slider_value = st.slider("Select a sentiment value:", -1.0, 1.0, 0.1)


    chart = alt.Chart(filtered_data).mark_bar().encode(
        x="yearmonth(date):O",
        y="average(polarity):Q",
        color="source:N"
    ).properties(
        width=600,
        height=300,
        title=f"Average Polarity for {selected_source}"
    )

    st.altair_chart(chart)


    p = figure(
        title='Simple Line Example',
        x_axis_label='x',
        y_axis_label='y')

    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    p.line(x, y, legend_label='Trend', line_width=2)

    st.write("## Bokeh Chart")
    st.bokeh_chart(p, use_container_width=True)

def main():
    media_selection()
    
if __name__ == "__main__":
    main()
