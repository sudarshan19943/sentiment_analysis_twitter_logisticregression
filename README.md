# Sentiment Analysis using Logistic Regression
This project performs sentiment analysis using a machine learning approach. Live tweets can be streamed and a thorough analysis of sentiments can be made using visualization graphs.

The project builds a data pipeline to demonstrate the ETL process. The stages of the ETL process is described below:
* Extraction - Extract live tweets using the Twitter API
* Transform - Cleaning of tweets using regex and use an ML model to evaluate tweet sentiments
* Load - Load the tweets and their sentiment values using elasicsearch

## General Instructions on using the application
Clone the project onto your local system and make sure you have installed Python 3.6.5 with Apache Spark version 2.3.2.

## Prerequisites
Before running the application on your system, make sure that it meets the following prerequisites:
* Download Python 3.6.5 from the following path: https://www.python.org/downloads/
* Download Apache Spark version 2.3.2 from the following link: https://spark.apache.org/downloads.html
* Make sure Java-8 JDK is present in your environment variables
* Download a lexicon with tweets and sentiment values.
* Create a developer account on Twitter and obtain the different security keys.

## Installing and Running
* Clone the project and run the following scripts in order: TweetStreaming.py, getelasticsearch.py, CountVectorizerImplementation.py, HashingTFImplementation.py and dataVisualizationOnSentiments.py

## Checking for errors
The project must be built first to check for any errors. For example, changes in the paths of packages could lead to a possible error. The build environment must be set with all environment variables intact.

## Executing the code
Run all the scripts in the order mentioned. The final graph containing the sentiment values of tweets is displayed on running the final script dataVisualizationOnSentiments.py

## Testing
A thorough manual testing has been done to check the functionality of the application in case of null values or exceptions.

### Results
Based on the sentiment scores calculated for each tweet, the results can be seen in sentiment_analysis_results.csv :)
