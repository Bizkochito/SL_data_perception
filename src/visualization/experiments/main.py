import pymongo
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
import re
import os
from dotenv import load_dotenv
import datetime
# from datetime import datetime, timedelta
from datetime import date
from datetime import datetime
import pytz

def get_articles(articles_limit=1000):
    load_dotenv()
    connection = os.getenv("MONGODB_URI")
    client = pymongo.MongoClient(connection)
    db = client.get_database ('bouman_datatank')
    col = db["articles"]
    news = col.find().limit(articles_limit)
    return news

news = get_articles()
df = pd.DataFrame(data=news)

df = df[df["date"].notna()]
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.sort_values(by="date")


all_sources = [i for i in df["source"].unique()]
fr_sources =  ['rtbf', 'lesoir', 'dhnet', 'lalibre', 'sudinfo', 'levif', 
'lavenir', 'lecho']
nl_sources =  ['tijd', 'demorgen', 'vrt', 'hln', 'knack']

def main():
    st.write("# Capstone Project \n  Belgian Newspaper Articles Sentiment Analysis on Data Related Topics ")
    st.sidebar.write("Capstone Project ")
    tabs = st.sidebar.radio("Select Functionality", ["Project Overview","Information on Data","Sentiment Analysis", "User Input"])
    if tabs == "Project Overview":
        st.write("### Project Overview \n Welcome to the Capstone Project, a collaboration between ***becode.org*** and ***the Data Tank***. Our project aims to delve into the fascinating world of public sentiment towards data and related topics in Belgium. By analyzing a vast collection of newspaper articles, we seek to gain valuable insights into how this sentiment has evolved over the years. ")
        st.write("### Collaborators")
        col2, col3, col1, col4, col5 = st.columns(5)
        with col2:
            becode_image = Image.open("./src/visualization/images/becode.png")
            st.image(becode_image,caption='Becode.org',width=100)
        with col3:
            data_tank_image = Image.open("./src/visualization/images/data_tank.png")
            st.image(data_tank_image,caption='the Data Tank',width=90)
        with col1:
            st.write("## ")
        with col4:
            st.write("## ")
        with col5:
            st.write("## ")
        st.write("### Objective \n In an era dominated by data-driven technologies and innovations, it's crucial to understand the public's perception and sentiment towards these topics. Our primary objective is to conduct sentiment analysis on a comprehensive dataset of Belgian newspaper articles. By employing advanced natural language processing techniques, we aim to:")
        st.write("""**Analyze Sentiment Trends:** Through the analysis of sentiment in news articles, we will uncover patterns and shifts in public opinion regarding data-related subjects. This will help us grasp how societal attitudes have changed over time.
                \n**Identify Key Themes:** Our analysis will identify prevalent themes within the articles, shedding light on the specific aspects of data that have garnered public attention and scrutiny.
                \n**Visualize Insights:** We will present our findings through visualizations that vividly illustrate sentiment trends and thematic evolution, providing an intuitive understanding of the data.""")
        st.write("""### Expected Impact \n Our project holds significant potential for various stakeholders, including policymakers, researchers, and the general public. By uncovering shifts in sentiment and identifying key concerns, we hope to contribute to informed decision-making and foster a deeper understanding of the societal implications of data-related advancements.
                \nFor inquiries or more information, please contact us at info@datatank.org""")


    elif tabs == "Information on Data":
        st.write("Information on Data")

        today = date.today()
        MIN_MAX_RANGE = (datetime(2019,1,1), datetime(2023,8,15))
        # MIN_MAX_RANGE = (datetime.datetime(2020,1,1), today)
        PRE_SELECTED_DATES = (datetime(2023,1,1), datetime(2023,8,1))
        selected_min, selected_max = st.slider(
            "Datetime slider",
            value=PRE_SELECTED_DATES,
            min_value=MIN_MAX_RANGE[0],
            max_value=MIN_MAX_RANGE[1],
        )
        mask = (df['date'] > selected_min) & (df['date'] <= selected_max)
        ne_df = df.loc[mask]

        new_df = ne_df.groupby(["source"]).size().reset_index(name='num_source')

        # st.sidebar.title("Filters")
        # start_dt = st.sidebar.date_input('start date', datetime.date(2020,1,1))
        # end_dt = df.iloc[-1]["date"]
        # # st.write(type(min_date))
        # # st.write(type(max_date))
        # slider = st.slider('Select date', min_value=start_dt, max_value=end_dt, format=format)

        # selected_date = st.sidebar.date_input("Select a date:", min_value=min_date, max_value=max_date)

        # Convert the selected_date back to a Pandas Timestamp if needed
        # selected_date_timestamp = pd.Timestamp.fromtimestamp(selected_date)

        # if selected_date:
        #     df_resampled = df.resample("D", on="date").sum()  # Resample daily

        #     # Display filtered data
        #     st.write("Filtered Data:")
        #     st.write(df_resampled.loc[selected_date.date()])  # Display data for selected date

        # # Weekly filter
        # weekly = st.sidebar.checkbox("Weekly")
        # if weekly:
        #     selected_week = st.sidebar.date_input("Select a week:", min_value=df["date"].min().date(), max_value=df["date"].max().date(), key="weekly")
        #     df_resampled = df.resample("W-MON", on="date").sum()  # Resample weekly starting on Monday
        #     st.write("Filtered Data:")
        #     st.write(df_resampled.loc[selected_week])

        # # Monthly filter
        # monthly = st.sidebar.checkbox("Monthly")
        # if monthly:
        #     selected_month = st.sidebar.date_input("Select a month:", min_value=df["date"].min().date(), max_value=df["date"].max().date(), key="monthly")
        #     df_resampled = df.resample("M", on="date").sum()  # Resample monthly
        #     st.write("Filtered Data:")
        #     st.write(df_resampled.loc[selected_month.replace(day=1):selected_month.replace(day=31)])

        # # Yearly filter
        # yearly = st.sidebar.checkbox("Yearly")
        # if yearly:
        #     selected_year = st.sidebar.date_input("Select a year:", min_value=df["date"].min().date(), max_value=df["date"].max().date(), key="yearly")
        #     df_resampled = df.resample("Y", on="date").sum()  # Resample yearly
        #     st.write("Filtered Data:")
        #     st.write(df_resampled.loc[selected_year.replace(month=1, day=1):selected_year.replace(month=12, day=31)])


        chart = (
            alt.Chart(new_df)
            .mark_bar()
            .encode(
                x=alt.X('source', axis=alt.Axis(title='Newspapers')),
                y=alt.Y('num_source', axis=alt.Axis(title='Articles Number')),
                # color='language',
            )
            .interactive()
        )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    elif tabs == "Sentiment Analysis":
        filtered_df = df
        selected_language = st.selectbox("Select Language", ["All", "fr", "nl"])
        if selected_language != "All":
            filtered_df = filtered_df[filtered_df['language'] == selected_language]
            if selected_language == "fr":
                default_selection = fr_sources
                selected_newspaper = st.multiselect("Select Newspaper(s) to Display", fr_sources)
                if selected_newspaper:
                    filtered_df = filtered_df[filtered_df["source"].isin(selected_newspaper)]
            elif selected_language == "nl":
                default_selection = nl_sources
                selected_newspaper = st.multiselect("Select Newspaper(s) to Display", nl_sources)
                if selected_newspaper:
                    filtered_df = filtered_df[filtered_df["source"].isin(selected_newspaper)]
        else:
            default_selection = all_sources
            selected_newspaper = st.multiselect("Select Newspaper(s) to Display", all_sources)
            if selected_newspaper:
                filtered_df = filtered_df[filtered_df["source"].isin(selected_newspaper)]
        

            # use_slider = st.checkbox("Use Sentiment Slider")
            # slider_value = 1.0
            # if use_slider:
            #     slider_value = st.slider("Select a sentiment value:", min_value= -1.0, max_value=1.0, value=[-1.0, 1.0])
            #     filtered_df = filtered_df[filtered_df['polarity'].between(slider_value[-1], slider_value[1])]

            chart = alt.Chart(filtered_df).mark_bar().encode(
                x=alt.X('date', title='Date'),
                y=alt.Y('mean(polarity):Q', title='Mean Polarity'),
                tooltip=['month:O', 'mean(polarity):Q'],
                # color=alt.Color("dataset:N", legend=alt.Legend(title="Topics"))
            ).properties(
                width=800,
                height=400,
                title='Mean Polarity by Date'
            )

        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    elif tabs == "User Input":
        

        test_start_date = st.date_input("Start Date")
        start_date = datetime.combine(test_start_date, datetime.min.time())

        # start_date = st.date_input("Start Date")

        test_end_date = st.date_input("End Date")
        end_date = datetime.combine(test_end_date, datetime.min.time())

        # end_date = st.date_input("End Date")

        # filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        mask = (df['date'] > start_date) & (df['date'] <= end_date)
        new_df = df.loc[mask]


        # MIN_MAX_RANGE = (datetime.datetime(2019,1,1), datetime.datetime(2023,8,15))
        # # MIN_MAX_RANGE = (datetime.datetime(2020,1,1), today)
        # PRE_SELECTED_DATES = (datetime.datetime(2023,1,1), datetime.datetime(2023,8,1))
        # selected_min, selected_max = st.slider(
        #     "Datetime slider",
        #     value=PRE_SELECTED_DATES,
        #     min_value=MIN_MAX_RANGE[0],
        #     max_value=MIN_MAX_RANGE[1],
        # )
        # mask = (df['date'] > selected_min) & (df['date'] <= selected_max)
        # ne_df = df.loc[mask]

        # Grouped bar chart
        bar_chart = alt.Chart(new_df).mark_bar().encode(
            x=alt.X("source:N", title="Source"),
            y=alt.Y("average(polarity):Q", title="Average Polarity"),
            # color=alt.Color("source:N", legend=None),
            tooltip=["source:N", "average(polarity):Q"]
        ).properties(
            width=600,
            height=400,
            title="Average Polarity by Source"
        )

        st.altair_chart(bar_chart, use_container_width=True)

if __name__ == "__main__":
    main()
