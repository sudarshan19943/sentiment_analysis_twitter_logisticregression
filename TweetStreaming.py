import tweepy
import socket
import json, csv
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sys
import re
#Twitter credentials
consumer_api_key = "BFphYY6qMnfqGRXwLBMSQ42f7"
consumer_api_secret = "MxGycobs7zC4vnAAD9HYfhvZ57MoBpucqPlTnVXaRqid1PXB6i"
access_token = "1044302133158445058-4k4K4aQphmxV6kTRBlLWtRckQzQmkU"
access_secret = "eQdWG2i8E0pdGcwBZ8lsLBNZ0uZt6uVeOLzlA9VxEY3Y4"

tweet_list = [] #Variable to store tweets

#Accessing Twitter API

#counter=1

#Class to stream live tweets
class TweetListener(tweepy.StreamListener):
	def __init__(self,api):
		self.counter = 1 #Initialize counter to limit the number of tweets to be streamed
		self.api=api

	def on_status(self, status):
		temp_dict = status.text #Obtaining the tweet statuses
		print("Tweets streamed: {}".format(self.counter))
		try:
			if temp_dict:
				self.counter += 1 #Incrementing for every tweet
				temp_dict = re.sub("https?:\/\/[^\s]*", "", temp_dict) #Cleaning every tweet
				temp_dict = re.sub("RT", "", temp_dict)
				temp_dict = re.sub("@[\w*]|#[\w*]|&[\w*]", "", temp_dict)
				temp_dict = re.sub("(@[\w*]|_|#|[\/\$%:!@#^&\*\(\)\|,\.\-;\"']|(\n))", "", temp_dict)
				temp_dict = re.sub("^[\w']*", " ", temp_dict)
				temp_dict = temp_dict.strip()
				if(temp_dict!= ""): 	
					tweet_list.append(temp_dict) #Storing cleaned tweet in a list

			if self.counter==2000: #Limiting tweets to 3000
				self.write_tweets_to_csv() #Write tweets to a file and exit
				sys.exit()
		except Exception as e:
			pass
		return True

	def write_tweets_to_csv(self):
		with open("twitter_tweets.csv", "w", newline='') as output_file: #Creating a csv file to store the tweets
			writer = csv.writer(output_file)
			writer.writerow(['text'])
			for val in tweet_list:
				writer.writerow([val.encode('ascii','ignore').decode('utf-8')])
		return

if __name__ == "__main__":
	auth = tweepy.OAuthHandler(consumer_api_key, consumer_api_secret) 
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	listener=TweetListener(api)
	twitterStream = Stream(auth=auth,listener=listener)  #Using Streaming API to stream live tweets
	twitterStream.filter(track=["Trump"]) #Obtaining tweets related to topic 'Trump'

