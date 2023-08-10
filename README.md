# Belgian Newspaper Articles Sentiment Analysis on Data Related Topics

This project was commissioned by DataTank to analyze sentiment around topics related to data from news articles published in Belgium. Using Streamlit for visualization, our objective is to understand the evolution of public sentiment towards data and related topics over time.


![LogoX](https://github.com/Bizkochito/SL_data_perception/assets/57298106/ff7c3375-e3b1-42dc-b80f-3c2dbc30d9c4)

## Database

Our data is sourced from scraping news articles from the top 20 Belgian newspapers since 2020, amassing around 3 million data points. We enriched this dataset with additional columns during preprocessing to enable a comprehensive analysis.

**Columns:** 
- url
- text
- title
- date
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

We utilize Streamlit for an interactive visualization of the results, providing users with a dynamic exploration experience.

## Teams

**Analytics Team:**
- Member 1
- Member 2
- Member 3
- Member 4
- Member 5

**Engineering Team:**
- Member 1
- Member 2
- Member 3
- Member 4
- Member 5

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




