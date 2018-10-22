import json, csv
import requests
from elasticsearch import Elasticsearch, helpers
#Function to load the file onto elasticsearch
def load_into_elasticsearch(infile):
	csvfile = open(infile, 'r')		#Convert the csv file to JSON file
	jsonfile = open('twitter_tweets.json', 'w')
	tweets = []
	fieldnames = ["text"]
	reader = csv.DictReader(csvfile, fieldnames)
	for row in reader:
		x={}
		x["text"]=row["text"]
		tweets.append(x)
	tweets.pop(0)
	json_obj = json.dumps(tweets)
	jsonfile.write(json_obj)
	csvfile.close()
	jsonfile.close()
	print("Inside Elasticsearch")
	URL = "https://portal-ssl1011-25.bmix-dal-yp-c9c45ba4-5394-401a-a2b1-99b3b97bfa2a.3040474850.composedb.com:58260"
	Index = "logisticregressionanalysis_17" 
	Type = "analysis_17" 
	port = 58260
	es = Elasticsearch(URL, port=port, http_auth=('admin','LKDGBXKDUDZWLYUU'))
	if es.ping(): 					#Checking connection with elastic search
		print("Connected!")
	else:
		print("Not Connected")
		
	request_body = {				#Structure of the request body
    	"settings" : {
        	"number_of_shards": 5,
        	"number_of_replicas": 0
   	 }
	}
		
	print("creating '%s' index..." % (Index)) #Creating index
	data = ""
	array_list = []
	array = {}
	count = 0
	with open ('twitter_tweets.json','r') as json_file:
		data = json.load(json_file)

	for val in data:
		array["_index"] = Index
		array["_type"] = Type
		count += 1
		array["_id"]=count
		array["_source"] = val
		array_list.append(array)
		array = {}
	res = helpers.bulk(es,array_list) #Bulk upload of tweets to elasticsearch

def get_from_elasticsearch():
	index = "logisticregressionanalysis_17"
	port = 58260
	URL = "https://portal-ssl1011-25.bmix-dal-yp-c9c45ba4-5394-401a-a2b1-99b3b97bfa2a.3040474850.composedb.com:58260"
	es = Elasticsearch(URL, port=port, http_auth=('admin','LKDGBXKDUDZWLYUU'))
	res = es.search(index=index, body="{\"query\": {\"match_all\": {}}}" ,size = 2000) #retrieving tweets using search method and limiting the tweets to 4000
	result = json.dumps(res)
	tweetsJson = json.loads(result)
	with open("test_input_file.csv","w", newline='') as opened_file: #dumping all loaded tweets into a CSV file
		writer = csv.writer(opened_file)
		writer.writerow(["text"])
		for jsonObj in tweetsJson["hits"]["hits"]:
			tweet = jsonObj["_source"]["text"].strip()
			if(tweet != "tweet"):
				writer.writerow([tweet])
load_into_elasticsearch('twitter_tweets.csv')
get_from_elasticsearch()