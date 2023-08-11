# Belgian Newspaper Articles Sentiment Analysis on Data Related Topics

This project was commissioned by [DataTank](https://datatank.org/) to analyze sentiment around topics related to data from news articles published in Belgium. Using Streamlit for visualization, our objective is to understand the evolution of public sentiment towards data and related topics over time.


![LogoX](https://github.com/Bizkochito/SL_data_perception/assets/57298106/ff7c3375-e3b1-42dc-b80f-3c2dbc30d9c4)

## Project Presentation

For a comprehensive overview of our project, its methodologies, and findings, please refer to our [presentation on Google Slides](https://docs.google.com/presentation/d/1jCWTUQgEO22PRISkzgC-LwYTkOgoQiVc_eluAiUNjbk/edit#slide=id.p).


## Project Workflow

Our project followed a structured workflow to ensure the quality and accuracy of the analysis:

1. **Data Collection (Scraping)**:
    - Articles were scraped from the top 20 Belgian newspapers since 2020.
    - The scraped data was then stored in a [MongoDB](https://www.mongodb.com/) database.

2. **Preprocessing**:
    - The data underwent a preprocessing stage where several columns were added to facilitate in-depth analysis. These columns include:
        - language
        - polarity
        - embedding
        - cos_score
        - data_related

3. **Analysis**:
    - Using the enriched data from the preprocessing stage, comprehensive analyses were conducted to answer the client's questions and derive meaningful insights from the data.


![schema](https://github.com/Bizkochito/SL_data_perception/assets/57298106/7bb36a2e-ba49-43ed-9372-463ba97a2f70)



## Database

Our data is sourced from scraping news articles from the top 20 Belgian newspapers since 2020, amassing around 3 million data points. We enriched this dataset with additional columns during preprocessing to enable a comprehensive analysis.


## Information on Data

**Scraped Columns:** 
- url
- text
- title
- date

**Columns from Preprocessing (for analysis):** 
- language
- polarity
- embedding
- cos_score
- data_related

**Languages:** 
- French
- Dutch

**Key Topics:** 
- Data use
- Data reusability
- Data reuse
- Data sharing
- Data access
- Data privacy
- Data protection

## Analysis Details

- **Language:** Identifies the article's language, facilitating segmented analysis.
- **Polarity:** Indicates the sentiment polarity of the article.
- **Embedding:** Vector representation of the article, useful for machine learning and similarity measurements.
- **Cos_score:** Likely a cosine similarity measure showing an article's relevance to a specific topic.
- **Data_related:** Binary indicator of the article's relevance to key data topics.

## Analysis Objective

We aim to answer:
- The overarching sentiment around data and its re-use in the Belgian news sector.
- The current dominant narrative regarding data.
- The evolution of this perception since 2020 and the impact of the pandemic.
- Sentiment variations between French and Dutch language newspapers.

## Results with Streamlit

Using [Streamlit](https://streamlit.io/), we've developed an interactive dashboard to visually present the results of our sentiment analysis. Here's a breakdown of our Streamlit application's capabilities:

1. **Project Overview Tab**: 
    - Introduces the objective of our project, emphasizing the importance of understanding public sentiment in today's data-driven era.
    - Highlights the expected impact and how our findings can benefit various stakeholders.
    - Provides contact information for further inquiries.

2. **Information on Data Tab**: 
    - Offers insights into our dataset, including the source, columns, languages, and the key topics we focused on.

3. **Sentiment Analysis Tab**: 
    - Displays comprehensive visualizations of sentiment trends derived from the data.
    - Allows users to filter and drill down into specific timeframes, topics, or sources to gain a deeper understanding of the sentiment patterns.
    - 
4. **User Input Tab**: 
    - Empowers users to input specific prompts or keywords.
    - Using semantic search, the system fetches articles that are contextually related to the provided input, ensuring relevant and meaningful results.
    - Presents both the articles themselves and sentiment visualizations based on the semantically retrieved articles for the inputted prompt.

## Teams

The teams are comprised of [Becode](https://becode.org/) trainees from the AI & Data Bootcamp training.

**Analytics Team:**
- [Ramina Chamileva](https://github.com/RamiRambo)
- [Yuliia Dranishcheva](https://github.com/Yuliia1701)
- [Mourad Amjahed](https://github.com/Mourad-Amj)
- [Sarkis Tadevosian](https://github.com/Ta-DevSark)
- [Grégoire Hupin](https://github.com/Bizkochito)
- [Maciej Krasowski](https://github.com/maciejkrsk)
- [Natalia Evgrafova](https://github.com/natalievgrafova)
- [Said Kardic](https://github.com/SaidKardic)
- [Marco](https://github.com/marcomisco)
- [Melikke Kaya](https://github.com/Melikkekaya)
- [Dastan Mirzayev](https://github.com/Dastan312)

**Engineering Team:**
- [Melih Orhan Yilmaz](https://github.com/melihorhanyilmaz)
- [Paul Strazzulla](https://github.com/Ptiful)
- [Mahmoud Hasan](https://github.com/MahmoudHasan83)
- [Sivasankari Subramani](https://github.com/ChristosRaptis)
- [Shankari Siva](https://github.com/sivasankari-subramani)
- [Volodymyr Savchuk](https://github.com/svstm)
    
## Technologies Used

- [Python 3.11](https://www.python.org/)
- [MongoDB](https://www.mongodb.com/)
- [Streamlit](https://streamlit.io/)
- [sentence-transformers (or Sentence Transformers)](https://github.com/UKPLab/sentence-transformers)
- [TextBlob](https://textblob.readthedocs.io/en/dev/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)

## Getting Started

### Installation

1. Clone this GitHub repository.
2. Install dependencies with `pip install -r requirements.txt`.
3. Confirm Python 3.10 or higher is installed.

### Running the Streamlit App

1. Navigate to the directory.
2. Execute `streamlit run app.py`.

Ensure all data files and scripts are correctly placed before initiating the Streamlit app.

## Challenges & Overcoming Them

Throughout this endeavor, we encountered challenges, notably in data scraping and sentiment analysis due to the multilingual nature of our sources. Collaborative efforts and the integration of robust tools and libraries ensured our results' accuracy and relevance.




