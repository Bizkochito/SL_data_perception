import pymongo
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from PIL import Image
import re
import os
from dotenv import load_dotenv
import datetime
import pytz
from sentence_transformers import SentenceTransformer, util

@st.cache_resource
def get_embedder():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def get_articles(limit):
    load_dotenv()
    connection = os.getenv("MONGODB_URI")
    client = pymongo.MongoClient(connection)
    db = client.get_database ('bouman_datatank')
    col = db["articles"]
    news = col.find(
        {
    "source": {
    "$exists": True,
    "$ne": None
    }}
    ).limit(limit)
    start = datetime.datetime.now()
    df = pd.DataFrame(data=news)
    df = df.drop("article", axis=1)
    df = df.dropna()
    print (datetime.datetime.now()-start)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date"].notna()]
    df["date"] = df["date"].apply(lambda dt: dt if dt.tzinfo else dt.replace(tzinfo=datetime.timezone.utc)).dt.date
    df = df.sort_values(by="date")
    return df

start = datetime.datetime.now()
df = get_articles(1000)
print (datetime.datetime.now()-start)

print("loaded","*"*50)

start_date = (df["date"].iloc[0])
end_date = (df["date"].iloc[-1])

all_sources = [i for i in df["source"].unique()]
fr_sources =  [i for i in df[df["language"]=="fr"]["source"].unique()]
nl_sources =  [i for i in df[df["language"]=="nl"]["source"].unique()]

def get_selected_df(df):
            subjects = ["All","Data Related", "Non Data Related"]
            selected_subject = st.selectbox("Select Subject to Display", subjects)
            if selected_subject == "Data Related":
                return df[df['data_related']==True]
            elif selected_subject == "Non Data Related":
                return df[df["data_related"]==False]
            elif selected_subject == "All":
                return df
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

def main():
    st.write("# Data Tank - Sentiment Analysis")
    st.sidebar.write("Data Tank Sentiment Analysis")
    tabs = st.sidebar.radio("Select Functionality", ["Project Overview","Information on Data","Sentiment Analysis", "User Input"])
    if tabs == "Project Overview":
        st.write("## Belgian Newspaper Articles Sentiment Analysis on Data Related Topics \n ### Project Overview \n This project was commissioned by DataTank to analyze sentiment around topics related to data from news articles published in Belgium. Our project aims to delve into the fascinating world of public sentiment towards data and related topics in Belgium. By analyzing a vast collection of newspaper articles, we seek to gain valuable insights into how this sentiment has evolved over the years. ")
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
                \n**Visualize Insights:** We will present our findings through visualizations that vividly illustrate sentiment trends and thematic evolution, providing an intuitive understanding of the data.""")
        st.write("""### Expected Impact \n Our project holds significant potential for various stakeholders, including policymakers, researchers, and the general public. By uncovering shifts in sentiment and identifying key concerns, we hope to contribute to informed decision-making and foster a deeper understanding of the societal implications of data-related advancements.
                \nFor inquiries or more information, please contact us at info@datatank.org""")


    elif tabs == "Information on Data":
        st.write("## Information on Data \n Analysis is made on a limited amount of data for demonstration purposes. After deployment, the queries can be made on the full dataset.")

        selected_df = get_selected_df(df)

        selected_option = st.selectbox("Time Frequency",  ["Day", "Week", "Month", "Year"])
        if selected_option == "Day":
            step = datetime.timedelta(days=1)
        elif selected_option == "Week":
            step = datetime.timedelta(weeks=1)
        elif selected_option == "Month":
            step = datetime.timedelta(days=30)  # Approximate number of days in a month
        elif selected_option == "Year":
            step = datetime.timedelta(days=365)  # Approximate number of days in a year

        selected_date_range = st.slider(
            "Select a date range",
            min_value=start_date,
            max_value=end_date,
            value=(start_date, end_date),
            step=step,
            format="DD/MM/YYYY",
        )
        
        mask = (selected_df['date'] >= selected_date_range[0]) & (selected_df['date'] <= selected_date_range[1])
        filtered_df = selected_df[mask]
        
        
      
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
                color='source',
            )
            .interactive()
        )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    elif tabs == "Sentiment Analysis":
        st.write("## Sentiment Analysis \n Analysis is made on a limited amount of data for demonstration purposes. After deployment, the queries can be made on the full dataset.")

        selected_df = get_selected_df(df)

        selected_option = st.selectbox("Time Frequency", ["Day", "Week", "Month", "Year"])

        if selected_option == "Day":
            step = datetime.timedelta(days=1)
        elif selected_option == "Week":
            step = datetime.timedelta(weeks=1)
        elif selected_option == "Month":
            step = datetime.timedelta(days=30)  # Approximate number of days in a month
        elif selected_option == "Year":
            step = datetime.timedelta(days=365)  # Approximate number of days in a year

        selected_date_range = st.slider(
            "Select a date range",
            min_value=start_date,
            max_value=end_date,
            value=(start_date, end_date),
            step=step,
            format="DD/MM/YYYY",
        )
        mask = (selected_df['date'] >= selected_date_range[0]) & (selected_df['date'] <= selected_date_range[1])
        test_df = selected_df[mask]
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
        embedder = get_embedder()
        input_client = st.text_input("Topic of articles to display : ")
        query_embedding = embedder.encode(input_client, convert_to_tensor=False)
        embeddings = np.array(df["embedding"].tolist()).astype(np.float32)
        cos_scores = util.cos_sim(query_embedding, np.array(df["embedding"].tolist()).astype(np.float32))
        results = df[(cos_scores[0] > .25).tolist()]
        columns = ["date","title","polarity","url"]

        st.dataframe(data=results[columns],hide_index=True)

if __name__ == "__main__":
    main()
