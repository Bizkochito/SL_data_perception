# Belgian Newspaper Articles Sentiment Analysis on Data Related Topics

This project was made for DataTank in the cadre of a Becode training. It focuses on analyzing sentiment around topics related to data from news articles published in Belgium. Using Streamlit for visualization, the objective is to gauge the evolution of public sentiment towards data and related topics over time.

![LogoX](https://github.com/Bizkochito/SL_data_perception/assets/57298106/ff7c3375-e3b1-42dc-b80f-3c2dbc30d9c4)

## Database

Our data is sourced from scraping news articles from the top 20 Belgian newspapers since 2020, resulting in around 3 million data points. During preprocessing, we enriched the data with additional columns to facilitate deeper analysis.

**Columns:** 
- source_url
- article_text
- article_title
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

- **Language:** Identifies the language of the article, aiding in segmenting analysis by linguistic group.
- **Polarity:** Represents the sentiment polarity of the article, which can range from very negative to very positive.
- **Embedding:** Contains the vector representation of the article, useful for various machine learning tasks and similarity measurements.
- **Cos_score:** Likely a measure of cosine similarity indicating how closely an article relates to a predefined vector or topic.
- **Data_related:** A binary column indicating whether the article is related to the key data topics of interest.

## Analysis Objective

Our analysis aims to answer:
- What is the overall sentiment around data and its re-use in the Belgian news sector?
- Is the current predominant narrative regarding data more negative than positive?
- How has this perception evolved since 2020? Is there a noticeable change before and after the pandemic?
- Is there a difference in sentiment between French or Dutch language newspapers?

## Results with Streamlit

We've employed Streamlit for interactive visualization of the results, offering users an intuitive way to explore the findings.

## Team

This project is driven by our dedicated analytics team:

- [Member 1](github_profile_link)
- [Member 2](github_profile_link)
- [Member 3](github_profile_link)
- [Member 4](github_profile_link)
- [Member 5](github_profile_link)

This project is driven by our dedicated engineers team:

- [Member 1](github_profile_link)
- [Member 2](github_profile_link)
- [Member 3](github_profile_link)
- [Member 4](github_profile_link)
- [Member 5](github_profile_link)

## Getting Started

### Installation

1. Clone this GitHub repository to your local machine.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Ensure you have Python 3.10 or higher installed.

### Running the Streamlit App

1. Navigate to the project directory.
2. Run the Streamlit app with `streamlit run app.py`.

Ensure all the data files and necessary scripts are in the appropriate directories before launching the Streamlit app.

## Challenges & Overcoming Them
## Du BLABLA
Throughout this project, we faced challenges, especially in data scraping and sentiment analysis due to the multilingual nature of the data. With collaboration and leveraging powerful tools and libraries, we ensured the accuracy and relevance of our results.




