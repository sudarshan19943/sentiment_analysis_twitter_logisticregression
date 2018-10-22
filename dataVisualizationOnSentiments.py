import matplotlib.pyplot as plt
import pandas as pd
#Counters to count positive, negative and neutral tweets
positive_counter = 0
neutral_counter = 0
negative_counter = 0
#Read into a dataframe
df = pd.read_csv('sentiment_analysis_results.csv')
sentiment_data = df['sentiment']
#Incrementing counters for each sentiment
for i in sentiment_data:
	if i == 'neutral':
		neutral_counter = neutral_counter + 1
	elif i == 'positive':
		positive_counter = positive_counter + 1
	elif i == 'negative':
		negative_counter = negative_counter + 1
#Setting plot values
left = [1, 2, 3] 
height = [neutral_counter, negative_counter, positive_counter] 

tick_label = ['Neutral', 'Negative', 'Positive'] 

value_bar = plt.bar(left, height, tick_label = tick_label, width = 0.8, color = ['blue', 'red', 'green']) 

for j in value_bar:
        height = j.get_height()
        plt.text(j.get_x() + j.get_width()/2., 1.05*height, '%d' % int(height), ha='center', va='bottom')
#Setting axis labels
plt.xlabel('X-axis as Sentiments') 
plt.ylabel('Y-axis as Number on Sentiment Counts') 

plt.title('Data Visualization on Test data') 

plt.show() 