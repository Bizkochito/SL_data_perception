import streamlit as st
import pandas as pd
import altair as alt
import random
from datetime import datetime, timedelta


sources_ref = ['rtbf.be', 'lesoir.be', 'dhnet.be', 'lalibre.be', 'sudinfo.be', 
'levif.be', 'lavenir.net', 'lecho.be', 'tijd.be', 
'demorgen.be', 'vrt.be', 'hln.be','knack.be']
fr_sources =  ['rtbf.be', 'lesoir.be', 'dhnet.be', 'lalibre.be', 'sudinfo.be', 'levif.be', 
'lavenir.net', 'lecho.be']
nl_sources =  ['tijd.be', 'demorgen.be', 'vrt.be', 'hln.be', 'knack.be']

def load_data(file_paths):
    dataframes = {}
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        dataframes[file_path] = df
    return dataframes

def generate_random_dates(num_dates):
    dates_list = []
    for _ in range(num_dates):
        random_year = random.randint(2000, 2023)
        random_month = random.randint(1, 12)
        random_day = random.randint(1, 28)  # Limit day to 28 to avoid invalid dates for February
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        random_date = datetime(random_year, random_month, random_day, random_hour, random_minute, random_second)
        dates_list.append(random_date)
    return dates_list

def random_date(start, end):
  return (start + datetime.timedelta(
      seconds=random.randint(0, int((end - start).total_seconds())))).isoformat()

@st.cache_data
def create_df(nb_records, dataset_name):
    headers = ["polarity", "source", "date", "title", "text", "language"]
    #200 articles
    polarities= [((random.randint(0,200)-100)/100) for x in range(nb_records)]
    # sources_ref = ["lesoir", "standaard", "rtbf"]
    sources = [random.sample(sources_ref, 1)[0] for x in range(nb_records)]
    dates = generate_random_dates(nb_records)
    languages_ref = ['fr', 'nl']
    languages = [random.sample(languages_ref, 1)[0] for x in range(nb_records)]
    datasets = [dataset_name for x in range(nb_records)]
    df =pd.DataFrame({"polarity": polarities, "source": sources, "date": dates, "language": languages, "dataset": datasets})
    df['date']  = pd.to_datetime(df['date'])
    df['month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
        # Group by month and calculate mean polarity
    #print(df)
    return df


def process_input(user_input):
    # Your processing logic here to generate a dataframe
    # For demonstration purposes, let's create a dummy dataframe
    data = {
        "source": ["Source A", "Source B", "Source A", "Source B"],
        "date": ["2023-08-01", "2023-08-01", "2023-08-02", "2023-08-02"],
        "polarity": [0.5, -0.2, 0.8, -0.5]
    }
    df = pd.DataFrame(data)
    return df

def main():
    st.title("Live Data Visualization App")

    # Tabs for different functionalities
    tabs = st.sidebar.radio("Select Functionality", ["Data Visualization", "User Input"])
    datasets_names = ["Data Related", "Non Data Related"]
    dataframes_list = [create_df(1000, "Data Related"), create_df(1000, "Non Data Related")]
    #indices = [x+1 for x in range(len(dataframes_list))]

    full_df = pd.concat(dataframes_list)
    if tabs == "Data Visualization":
        # Upload CSV files
        uploaded_files = True #st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
        if uploaded_files:
            # Checkbox to select dataframes
            selected_dataframes = st.multiselect("Select Dataframes to Display", datasets_names, [datasets_names[0]])
            if selected_dataframes:
                filtered_df = full_df[full_df['dataset'].isin(selected_dataframes)]

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
                    default_selection = sources_ref
                    selected_newspaper = st.multiselect("Select Newspaper(s) to Display", sources_ref)
                    if selected_newspaper:
                        filtered_df = filtered_df[filtered_df["source"].isin(selected_newspaper)]
                

                # use_slider = st.checkbox("Use Sentiment Slider")
                # slider_value = 1.0
                # if use_slider:
                #     slider_value = st.slider("Select a sentiment value:", min_value= -1.0, max_value=1.0, value=[-1.0, 1.0])
                #     filtered_df = filtered_df[filtered_df['polarity'].between(slider_value[-1], slider_value[1])]

                chart = alt.Chart(filtered_df).mark_bar().encode(
                    x=alt.X('month:O', title='Month'),
                    y=alt.Y('mean(polarity):Q', title='Mean Polarity'),
                    tooltip=['month:O', 'mean(polarity):Q'],
                    color=alt.Color("dataset:N", legend=alt.Legend(title="Topics"))
                ).properties(
                    width=800,
                    height=400,
                    title='Mean Polarity by Month'
                )
                # Altair plot
                # chart = alt.Chart(plot_data).mark_line().encode(
                #     x="date:T",
                #     y="polarity:Q",
                #     color=alt.Color("dataset:N", legend=alt.Legend(title="Topics")),
                #     tooltip=["date:T", "polarity:Q", "dataset:N"]
                # ).properties(
                #     width=800,
                #     height=400
                # ).interactive()

                # Display the chart
                st.altair_chart(chart, use_container_width=True)
        
    elif tabs == "User Input":
        st.title("User Input and Visualization")

        # User input text prompt
        user_input = st.text_input("Enter some input:")
        if user_input:
            processed_df = process_input(user_input)

            # Date range slider
            start_date = st.date_input("Start Date", processed_df["date"].min())
            end_date = st.date_input("End Date", processed_df["date"].max())

            filtered_df = processed_df[(processed_df["date"] >= start_date) & (processed_df["date"] <= end_date)]

            # Grouped bar chart
            bar_chart = alt.Chart(filtered_df).mark_bar().encode(
                x=alt.X("source:N", title="Source"),
                y=alt.Y("average(polarity):Q", title="Average Polarity"),
                color=alt.Color("source:N", legend=None),
                tooltip=["source:N", "average(polarity):Q"]
            ).properties(
                width=600,
                height=400,
                title="Average Polarity by Source"
            )

            st.altair_chart(bar_chart, use_container_width=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
