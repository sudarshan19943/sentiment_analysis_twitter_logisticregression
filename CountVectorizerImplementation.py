from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer, CountVectorizer
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.types import IntegerType
import pandas as pd
import re
import csv
import time

start_time = time.time()
sc = SparkContext() #Creates a spark context
spark = SQLContext(sc) #Using spark SQLContext  
clean_tweets_list = []
df = pd.read_csv('Tweets.csv') #Converting training data into dataframe using pandas

#Cleaning of tweets
def clean_tweet(tweet):
    textinp = (re.sub("https?:\/\/[^\s]*", "", tweet))
    textinp = re.sub("RT", "", textinp)
    textinp = re.sub("@[\w*]|#[\w*]|&[\w*]", "", textinp)
    textinp = textinp.lower()
    textinp = textinp.strip()
    return textinp

#Labelling of tweets based on sentiment scores
def labelling(sentimentscore):
  if sentimentscore == "neutral":
    return  float(1.0)
  elif sentimentscore == 'negative':
    return float(0.0)
  elif sentimentscore == 'positive':
    return float(2.0)
    

sentiment_df = df['airline_sentiment'].apply(labelling) #Storing sentiment scores in a dataframe
tweet_df = df['text'].apply(clean_tweet) #Storing cleaned tweets in a dataframe
merge_df = pd.concat([tweet_df, sentiment_df],axis=1) #Adding columns tweets and sentiments to a single dataframe
merge_df.columns = ["text","label"] #The column labels of the dataframe
merge_df = merge_df.drop_duplicates(["text"]) #Removing duplicate tweets (if any)

merge_df.to_csv('training_input_file.csv',index=False) #Storing the dataframe as a csv file


# Prepare training documents from a list of (text, label) tuples using a training input file.
training = spark.read.format("csv").option("header","true").load("training_input_file.csv") #load the training file
training = training.withColumn("label", training.label.cast(IntegerType())) #Adding a label column to existing table
training = training.dropna() #Dropping null values in the tweets

(train_set, validation_set) = training.randomSplit([0.90, 0.10]) #Splitting training set and validation set as 90% and 10% respectively

# Configuring a pipeline, which consists of three stages: tokenizer, CountVectorizer, and LogisticRegression.
tokenizer = Tokenizer(inputCol="text", outputCol="words")
countvect = CountVectorizer(inputCol=tokenizer.getOutputCol(), outputCol="features")
lr = LogisticRegression(maxIter=10, regParam=0.001)
pipeline = Pipeline(stages=[tokenizer, countvect, lr])

# Fit the pipeline to training documents by creating a model.
model = pipeline.fit(train_set)
#Creating a prediction set
prediction_validation_set = model.transform(validation_set)
#Calculation of accuracy
accuracy = prediction_validation_set.filter(prediction_validation_set.label == prediction_validation_set.prediction).count() / float(validation_set.count())
print ("Accuracy Score: {0:.4f}%".format(accuracy * 100))

# Prepare test documents
test = spark.read.format("csv").option("header","true").load("test_input_file.csv")
test = test.dropna()

# Make predictions on test documents and print columns of interest.
prediction = model.transform(test)

selected = prediction.select("text", "prediction")
with open("sentiment_analysis_results.csv","w",newline='') as f:
  writer = csv.writer(f)
  writer.writerow(["text","sentiment"])
  for row in selected.collect():
      text, prediction = row
      if int(prediction) == 0:
        senti = "negative"
      elif int(prediction) == 1:
        senti = "neutral"
      elif int(prediction) == 2:
        senti = "positive"
      writer.writerow([text.encode("ascii").decode("utf-8"),senti])
end_time = time.time()
print("Time taken: {0:.4f}".format(end_time-start_time))