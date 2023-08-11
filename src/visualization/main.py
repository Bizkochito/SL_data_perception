import pymongo
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
import re
import os
from dotenv import load_dotenv
import datetime
from datetime import timedelta
from datetime import date
from datetime import datetime, timedelta
import pytz
from sentence_transformers import SentenceTransformer, util

st.set_page_config(layout="wide")

def get_articles(articles_limit=5000):
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
# df = df.sort_values(by="date")
# min_date = pd.to_datetime(df["date"].iloc[0])
# max_date = pd.to_datetime(df["date"].iloc[-1])

# df['month'] = df["date"].dt.to_period("M")
# monthly_avg = df.groupby('month')['polarity'].mean()
# df['avg_polarity'] = df['month'].map(monthly_avg)

all_sources = [i for i in df["source"].unique()]
fr_sources =  [i for i in df[df["language"]=="fr"]["source"].unique()]
nl_sources =  [i for i in df[df["language"]=="nl"]["source"].unique()]

def main():
    st.write("# Data Tank")
    st.sidebar.write("Data Tank Sentiment Analysis")
    tabs = st.sidebar.radio("Select Functionality", ["Project Overview","Information on Data","Sentiment Analysis", "User Input"])
    if tabs == "Project Overview":
        st.write("## Belgian Newspaper Articles Sentiment Analysis on Data Related Topics \n ### Project Overview \n Welcome to the Capstone Project, a collaboration between ***becode.org*** and ***the Data Tank***. Our project aims to delve into the fascinating world of public sentiment towards data and related topics in Belgium. By analyzing a vast collection of newspaper articles, we seek to gain valuable insights into how this sentiment has evolved over the years. ")
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
        st.write("## Information on Data")
        
        start_date = datetime(2020,1,1)
        end_date = datetime(2023,8,10)

        selected_option = st.selectbox("Select Date Range Option", ["Day", "Week", "Month", "Year"])

        if selected_option == "Day":
            step = timedelta(days=1)
        elif selected_option == "Week":
            step = timedelta(weeks=1)
        elif selected_option == "Month":
            step = timedelta(days=30)  # Approximate number of days in a month
        elif selected_option == "Year":
            step = timedelta(days=365)  # Approximate number of days in a year

        selected_date_range = st.slider(
            "Select a date range",
            min_value=start_date,
            max_value=end_date,
            value=(start_date, end_date),
            step=step,
            format="DD/MM/YYYY",
        )

        mask = (df['date'] >= selected_date_range[0]) & (df['date'] <= selected_date_range[1])
        filtered_df = df[mask]
      
        # source_counts = filtered_df.groupby(["source"]).size().reset_index(name='num_source')
        # source_counts_sorted = filtered_df.groupby(["source"]).size().reset_index(name='num_source').sort_values("num_source",ascending=False)

        # chart = (
        #     alt.Chart(source_counts)
        #     .mark_bar()
        #     .encode(
        #         x=alt.X('source', axis=alt.Axis(title='Newspapers')),
        #         y=alt.Y('num_source', axis=alt.Axis(title='Articles Number')),
        #         # color='language',
        #     )
        #     .interactive()
        # )
        # st.altair_chart(chart, theme="streamlit", use_container_width=True)

        st.write("### Number of Articles per Newspaper")
        # st.dataframe(data=source_counts_sorted,hide_index=True)

        chart = (
            alt.Chart(filtered_df)
            .mark_bar()
            .encode(
                x=alt.X('source:N', axis=alt.Axis(title='Newspapers')),
                y=alt.Y('count(source):Q', axis=alt.Axis(title='Articles Number')),
                # color='source',
            )
            .interactive()
        )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    elif tabs == "Sentiment Analysis":
        start_date = datetime(2020,1,1)
        end_date = datetime(2023,8,10)

        selected_option = st.selectbox("Select Date Range Option", ["Day", "Week", "Month", "Year"])

        if selected_option == "Day":
            step = timedelta(days=1)
        elif selected_option == "Week":
            step = timedelta(weeks=1)
        elif selected_option == "Month":
            step = timedelta(days=30)  # Approximate number of days in a month
        elif selected_option == "Year":
            step = timedelta(days=365)  # Approximate number of days in a year

        selected_date_range = st.slider(
            "Select a date range",
            min_value=start_date,
            max_value=end_date,
            value=(start_date, end_date),
            step=step,
            format="DD/MM/YYYY",
        )
        # selected_date_range = st.slider(
        #     "Select a date range",
        #     min_value=min_date,
        #     max_value=max_date,
        #     value=(min_date, max_date),
        #     step=step,
        #     format="DD/MM/YYYY",
        # )
        mask = (df['date'] >= selected_date_range[0]) & (df['date'] <= selected_date_range[1])
        test_df = df[mask]

        def get_filtered_df(df):
            selected_language = st.selectbox("Select Language", ["All", "French", "Dutch"])
            if selected_language == "French":
                default_selection = fr_sources
                selected_newspaper = st.multiselect("Select Newspaper(s) to Display", fr_sources, default=default_selection)
                filtered_df = df[df["source"].isin(selected_newspaper)]
                return filtered_df
            elif selected_language == "Dutch":
                default_selection = nl_sources
                selected_newspaper = st.multiselect("Select Newspaper(s) to Display", nl_sources, default=default_selection)
                filtered_df = df[df["source"].isin(selected_newspaper)]
                return filtered_df
            elif selected_language not in ["French","Dutch"]:
                default_selection = all_sources
                selected_newspaper = st.multiselect("Select Newspaper(s) to Display", all_sources, default=default_selection)
                filtered_df = df[df["source"].isin(selected_newspaper)]
                return filtered_df
            # else:
            #     default_selection = all_sources
            #     selected_newspaper = st.multiselect("Select Newspaper(s) to Display", all_sources,default=default_selection)
            #     filtered_df = df[df["source"].isin(selected_newspaper)]
            #     return filtered_df
        
        filtered_df = get_filtered_df(test_df)

        use_slider = st.checkbox("Use Sentiment Slider")
        if use_slider:
            selected_polarity_range = st.slider(
            "Select a polarity range",
            min_value=-1.0,
            max_value=1.0,
            value=(-1.0, 1.0))
            mask = (df['polarity'] >= selected_polarity_range[0]) & (df['polarity'] <= selected_polarity_range[1])
            filtered_df = filtered_df[mask]

        chart = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('date', title='Date'),
            y=alt.Y('mean(polarity):Q', title='Polarity Score'),
            # tooltip=['month:O', 'mean(polarity):Q'],
            # color=alt.Color("dataset:N", legend=alt.Legend(title="Topics"))
        ).properties(
            width=800,
            height=400,
            title='Mean Polarity by Date'
        ).interactive()

        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    elif tabs == "User Input":
        st.write("This interface serves as your access point to a carefully curated collection of articles designed to align with your interests. To begin, kindly provide us with either specific keywords or a concise prompt. Our advanced algorithm will then diligently select a range of relevant articles from our comprehensive database.")
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        load_dotenv()
        connection = os.getenv("MONGODB_URI")
        client = pymongo.MongoClient(connection)
        db = client.get_database ('bouman_datatank')
        col = db["articles"]
        cursor = col.find({"embedding":{"$exists":True}})

        input_client = st.text_input("Topic of articles to display : ")
        query = [str(input_client)]

        query_embedding = embedder.encode(query, convert_to_tensor=False)

        dico_list = []
        
        for doc in cursor:
            # st.write(doc)
            doc_dico = {}
            cos_score = util.cos_sim(query_embedding, doc["embedding"])[0]
            if cos_score.abs() > 0.25:
                doc_dico["polarity"] = doc["polarity"]
                doc_dico["source"] = doc["source"]
                doc_dico["language"] = doc["language"]
                doc_dico["date"] = doc["date"]
                doc_dico["url"] = doc["url"]
                dico_list.append(doc_dico)

        df_output = pd.DataFrame(dico_list)
        st.dataframe(data=df_output,hide_index=True)

if __name__ == "__main__":
    main()
