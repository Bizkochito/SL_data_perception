import pymongo
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

all_sources = ['rtbf.be', 'lesoir.be', 'dhnet.be', 'lalibre.be', 'sudinfo.be', 
'levif.be', 'lavenir.net', 'lecho.be', 'tijd.be', 
'demorgen.be', 'vrt.be', 'hln.be','knack.be']

fr_sources =  ['rtbf.be', 'lesoir.be', 'dhnet.be', 'lalibre.be', 'sudinfo.be', 'levif.be', 
'lavenir.net', 'lecho.be']
nl_sources =  ['tijd.be', 'demorgen.be', 'vrt.be', 'hln.be', 'knack.be']

def get_articles(articles_limit):
    connection = "mongodb://bouman:80um4N!@ec2-15-188-255-64.eu-west-3.compute.amazonaws.com:27017/"
    client = pymongo.MongoClient(connection)
    db = client.get_database ('bouman_datatank')
    col = db["articles"]
    news = col.find().limit(articles_limit)
    # df = pd.DataFrame(data=news)
    return news




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
        st.write(df.head(10))
    #     st.write("")
    #     chart = (
    #         alt.Chart(df)
    #         .mark_circle()
    #         .encode(
    #             x="date",
    #             y='avg_polarity',
    #             color='newspaper'
    #         )
    #         .interactive()
    #     )

    #     st.altair_chart(chart, theme="streamlit", use_container_width=True)

if __name__ == "__main__":
    main()
