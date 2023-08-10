import streamlit as st
import numpy as np
import datetime
import altair as alt
from bokeh.plotting import figure
import pandas as pd
import matplotlib.pyplot as plt

def random_date(start, end):
    return (start + datetime.timedelta(
        seconds=np.random.randint(0, int((end - start).total_seconds())))).isoformat()

def create_df():
    polarities = [((np.random.randint(0, 200) - 100) / 100) for _ in range(200)]
    sources_ref = ["lesoir", "standaard", "rtbf"]
    sources = [np.random.choice(sources_ref) for _ in range(200)]
    dates = [random_date(datetime.datetime(2010, 1, 1), datetime.datetime(2021, 1, 12)) for _ in range(200)]
    languages_ref = ['fr', 'nl', 'All']
    languages = [np.random.choice(languages_ref) for _ in range(200)]

    return pd.DataFrame({"polarity": polarities, "source": sources, "date": dates, "language": languages})

def media_selection():
    st.title("Media Selection")

    data = create_df()

    sources = sorted(data['source'].unique())
    languages = sorted(data['language'].unique())

    language = st.selectbox("Select a language:", languages)
    selected_source = st.selectbox("Select a source:", sources)

    filtered_data = data[(data["source"] == selected_source) & (data["language"] == language)]

    use_slider = st.checkbox("Use Sentiment Slider")
    slider_value = 1.0

    if use_slider:
        slider_value = st.slider("Select a sentiment value:", -1.0, 1.0, 0.1)

    # Create a sample DataFrame
    data_sample = {'Value': [-0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]}
    data_frame = pd.DataFrame(data_sample)

    # Filter DataFrame based on slider value or default value
    filtered_data = data_frame[data_frame['Value']<= slider_value]

    # Display filtered data
    st.write("Filtered Data:")
    st.write(filtered_data)

    # Plot the chart
    plt.figure(figsize=(8, 6))
    plt.scatter(filtered_data['Value'], filtered_data['Year'], color='blue', label='Filtered Data')
    plt.xlabel('Value')
    plt.ylabel('Year')
    plt.title('Chart')
    plt.legend()
    st.pyplot(plt)

def main():
    media_selection()
    
if __name__ == "__main__":
    main()