import pymongo
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
import re
import os
from dotenv import load_dotenv


all_sources = ['rtbf.be', 'lesoir.be', 'dhnet.be', 'lalibre.be', 'sudinfo.be', 
'levif.be', 'lavenir.net', 'lecho.be', 'tijd.be', 
'demorgen.be', 'vrt.be', 'hln.be','knack.be']

fr_sources =  ['rtbf.be', 'lesoir.be', 'dhnet.be', 'lalibre.be', 'sudinfo.be', 'levif.be', 
'lavenir.net', 'lecho.be']
nl_sources =  ['tijd.be', 'demorgen.be', 'vrt.be', 'hln.be', 'knack.be']

def get_articles(articles_limit):
    load_dotenv()
    connection = os.getenv("MONGODB_URI")
    client = pymongo.MongoClient(connection)
    db = client.get_database ('bouman_datatank')
    col = db["articles"]
    news = col.find().limit(articles_limit)
    return news

news = get_articles(10)
df = pd.DataFrame(data=news)

df['newspaper'] = df['url'].map(lambda x: re.search(r'://(?:www\.)?([a-zA-Z0-9.-]+)', str(x)).group(1))
def get_language(newspaper):
    if newspaper in fr_sources:
        return "fr"
    elif newspaper in nl_sources:
        return "nl"
    else:
        "unknown"
df['language'] = df['newspaper'].apply(get_language)


def main():
    st.write("# BeCode Capstone Project \n  Belgian Newspaper Articles Sentiment Analysis on Data Related Topics ")
    st.sidebar.write("BeCode Capstone Project ")
    tabs = st.sidebar.radio("Select Functionality", ["Project Overview","Information on Data","Sentiment Analysis", "User Input"])
    
    if tabs == "Project Overview":
        st.write("### Project Overview \n Welcome to the BeCode Capstone Project, a collaboration between ***becode.org*** and ***the Data Tank***. Our project aims to delve into the fascinating world of public sentiment towards data and related topics in Belgium. By analyzing a vast collection of newspaper articles, we seek to gain valuable insights into how this sentiment has evolved over the years. ")
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
    #     st.write("")
        chart = (
            alt.Chart(df)
            .mark_circle()
            .encode(
                x="date",
                y='avg_polarity',
                color='newspaper'
            )
            .interactive()
        )
    elif tabs == "Sentiment Analysis":
        
        # Upload CSV files
        # uploaded_files = True #st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
        # if uploaded_files:
            # Checkbox to select dataframes
        # selected_dataframes = st.multiselect("Select Dataframes to Display", datasets_names, [datasets_names[0]])
        # if selected_dataframes:
            # filtered_df = full_df[full_df['dataset'].isin(selected_dataframes)]
        filtered_df = df
        selected_language = st.selectbox("Select Language", ["All", "fr", "nl"])
        if selected_language != "All":
            filtered_df = filtered_df[filtered_df['language'] == selected_language]
            if selected_language == "fr":
                default_selection = fr_sources
                selected_newspaper = st.multiselect("Select Newspaper(s) to Display", fr_sources)
                if selected_newspaper:
                    filtered_df = filtered_df[filtered_df["newspaper"].isin(selected_newspaper)]
            elif selected_language == "nl":
                default_selection = nl_sources
                selected_newspaper = st.multiselect("Select Newspaper(s) to Display", nl_sources)
                if selected_newspaper:
                    filtered_df = filtered_df[filtered_df["newspaper"].isin(selected_newspaper)]
        else:
            default_selection = all_sources
            selected_newspaper = st.multiselect("Select Newspaper(s) to Display", all_sources)
            if selected_newspaper:
                filtered_df = filtered_df[filtered_df["newspaper"].isin(selected_newspaper)]
        

            # use_slider = st.checkbox("Use Sentiment Slider")
            # slider_value = 1.0
            # if use_slider:
            #     slider_value = st.slider("Select a sentiment value:", min_value= -1.0, max_value=1.0, value=[-1.0, 1.0])
            #     filtered_df = filtered_df[filtered_df['polarity'].between(slider_value[-1], slider_value[1])]

            # chart = alt.Chart(filtered_df).mark_line().encode(
            #     x=alt.X('month:O', title='Month'),
            #     y=alt.Y('mean(polarity):Q', title='Mean Polarity'),
            #     tooltip=['month:O', 'mean(polarity):Q'],
            #     color=alt.Color("dataset:N", legend=alt.Legend(title="Topics"))
            # ).properties(
            #     width=800,
            #     height=400,
            #     title='Mean Polarity by Month'
            # )
            chart = (
            alt.Chart(df)
            .mark_circle()
            .encode(
                x= 'date',
                y='polarity',
            )
            .interactive()
        )
        # st.altair_chart(chart, theme="streamlit", use_container_width=True)

if __name__ == "__main__":
    main()
