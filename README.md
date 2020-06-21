# Technology_NLP

## Introduction 
The goal of my analysis was to determine how the general attitude towards technology has changed over time. This was done by applying machine learning techniques, specifically sentiment analysis and topic analysis, to New York Times articles from different time periods.

## Data Collection
To create the dataset, I used the New York Times Article Search API: https://developer.nytimes.com/docs/articlesearch-product/1/overview. 
The API retrieves the urls of the most relevant articles for a given search term and timeframe. I used the search term 'technology' to get the urls of the top 30 results for each month from January 1980 to December 2019. I then used web scraping to retrieve the body text of each of the articles from their urls. The resulting dataset contains the body text of the top 1440 New York Times articles about technology by date. 

## Sentiment Analysis

### Method
Sentiment analysis is a machine learning technique used to interpret and classify the emotions in a given piece of text. To implement this technique on the dataset, I first used the NRC Emotion Lexicon to map each word in the dictionary to the emotions that it is associated with. Each word can be associated with any number of the following emotions (a word may also not be associated with any emotion):

* anger
* fear 
* anticipation 
* trust
* surprise
* sadness 
* joy
* disgust

Then for each piece of text, the sum of all the words associated with each of the emotions was counted and then the value was normalized by the total number of words in the text to get a final score for each emotion. I then found the average score for each emotion for each month. 

## Topic Analysis

### Method
In order to understand to get a better understanding of the resulting trends, I conducted a topic analysis on the texts aggregated by decade. This is a technique to extract meaning from a text by identifying recurring themes or topics that best describe the set of documents. I used the Latent Dirichlet Allocation (LDA) model to extract 25 topics for each decade. 



