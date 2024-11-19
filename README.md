# Enhancing Singapore Airlines' Service Through Automated Sentiment Analysis of Customer Reviews

## Project Overview

This project focuses on performing sentiment analysis on customer reviews of Singapore Airlines. The goal is to analyze customer sentiments over time to identify trends, improve service quality, and enhance customer satisfaction.

### Objectives:

-   Utilise a myriad of classification models to determine the best performing model.
-   Use NLP techniques to analyze and classify sentiments as positive, neutral or negative.

---

## Table of Contents

1. [Project Setup](#project-setup)
2. [Installation](#installation)
3. [Dataset](#dataset)
4. [Data Collection](#data-collection)
5. [Description of Notebooks](#description-of-notebooks)
6. [Contributors](#contributors)

---

## Project Setup

Before running the project, ensure you have the required libraries installed. The project is based on Python and utilizes several NLP and machine learning libraries.

---

## Installation

To set up the environment, follow these steps:

1.  Clone the repository:

        git clone https://github.com/hyinki/mla.git

2.  Navigate to the project directory:

        cd mla

3.  Create a virtual environment:

        python -m venv venv

    source venv/bin/activate # For Linux/macOS
    venv\Scripts\activate # For Windows

4.  Install the required dependencies:

        pip install -r requirements.txt

The requirements.txt file includes the following packages:

-   pandas
-   numpy
-   scipy
-   tqdm
-   matplotlib
-   seaborn
-   langdetect
-   langid
-   nltk
-   spacy
-   wordcloud
-   scikit-learn
-   tensorflow
-   torch
-   transformers
-   tokenizers
-   keras
-   gensim

---

## Datasets

The project uses a labelled dataset of 10,000 anonymised customer reviews on Singapore Airlines, which can be downloaded from Kaggle. This dataset provides the foundational data for training the models.

-   **Kaggle Dataset link:** [Kaggle: Singapore Airlines Reviews Dataset](https://www.kaggle.com/datasets/kanchana1990/singapore-airlines-reviews)

We also decided to scrape for more customer reviews of Singapore Airlines from TripAdvisor and Skytrax.

-   **TripAdvisor Link** https://www.tripadvisor.com.sg/Airline_Review-d8729151-Reviews-Singapore-Airlines
-   **Skytrax Link** https://www.airlinequality.com/airline-reviews/singapore-airlines/?sortby=post_date%3ADesc&pagesize=100

Brief Description of `csv` files:

-   `singapore_airlines_reviews.csv`: from Kaggle dataset.
-   `singapore_airlines_reviews_tripadvisor.csv`: scraped from TripAdvisor.
-   `singapore_airlines_reviews_skytrax.csv`: scraped from Skytrax
-   `final_df.csv`: Combined all 3 previous csv files and performed basic preprocessing such as Tokenization and Porter Stemmer, this csv file is created from `preprocessing.ipynb`.

## Data Collection

The structure of the dataset is as follows:

-   **`published_date`**: Date and time of review publication.
-   **`published_platform`**: Platform where the review was posted.
-   **`rating`**: Customer satisfaction rating, from 1 (lowest) to 5 (highest).
-   **`type`**: Specifies the content as a review.
-   **`text`**: Detailed customer feedback.
-   **`title`**: Summary of the review.
-   **`helpful_votes`**: Number of users finding the review helpful.

---

## Description of notebooks

── model_experiments<br>
│ ├── `BERT.ipynb` <br>
│ ├── `CNN.ipynb`<br>
│ ├── `DistilBERT.ipynb`<br>
│ ├── `ELECTRA.ipynb`<br>
│ ├── `GRU.ipynb`<br>
│ ├── `Llama3.2.ipynb`<br>
│ ├── `LSTM.ipynb`<br>
│ ├── `NN.ipynb`<br>
│ ├── `RNN.ipynb`<br>
│ ├── `SVM.ipynb`<br>
├── processing_experiments<br>
│ ├── `EDA.ipynb` Conducted initial EDA<br>
│ ├── `fasttext.ipynb` Applied FastText to baseline models<br>
│ ├── `lemmatization.ipynb` Experimented with lemmatisation for text preprocessing<br>
│ ├── `porterstemmer.ipynb` Experimented with porter stemmer for text preprocessing<br>
│ ├── `preprocessing.ipynb` Created `final_df.csv` after deciding on Porter Stemmer<br>
│ ├── `snowballstemmer.ipynb` Experimented with snowball stemmer for text preprocessing<br>
│ ├── `word2vec.ipynb` Applied Word2Vec to baseline models<br>

---

## Contributors

This project was developed by:

-   Shaun Zhou
    [GitHub](https://github.com/shaunzzhou)
-   Darius Ng
    [GitHub](https://github.com/dariusnggg)
-   Hyin Ki
    [GitHub](https://github.com/hyinki)
-   John Tan
    [GitHub](https://github.com/JohnErnestTan)
-   May
    [GitHub](https://github.com/May-mnaung)
-   Ritika Bajpai
    [GitHub](https://github.com/ritikabaj)

---
