from matplotlib.axes import Axes
from matplotlib import pyplot as plt
import numpy as np
import tweepy
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY= os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
endpoint = os.getenv('endpoint')
ta_credential = os.getenv('ta_credential')
key = os.getenv('key')

#Creates a twitter client and fetches recent tweets given a search query.
def twitter_client(response):
    search_term = response
    client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY, consumer_secret=API_SECRET_KEY, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET, return_type=dict, wait_on_rate_limit=False)
    return client.search_recent_tweets(f'{search_term} lang:en -is:retweet')

#Creates and initializes an Azure client
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

#Creates a bar graph and a histogram based on the data that was returned
def graph_data(doc_sentiments):
    labels = ['positive', 'neutral', 'negative']
    x = np.arange(len(labels))
    width = 0.35
    
    fig, axes = plt.subplots(1, 2, figsize=(8, 8))
    axes[0].bar(labels, doc_sentiments, width)
    axes[0].set_ylabel('Number of Documents by Sentiment')
    axes[0].set_title('Sentiments for Given Topic (Recent Tweet Criteria)')
    
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
    axes[1].pie(doc_sentiments, labels=labels, colors=colors, radius=3, center=(4, 4), wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
    plt.plot()
    plt.show()

#takes the azure client and a parsed set of tweets and returns the sentiment scores
def sentiment_analysis(client, parsed_tweets):
    result = client.analyze_sentiment(parsed_tweets)
    doc_result = [doc for doc in result if not doc.is_error]
    doc_sentiments = [[document.confidence_scores.positive, document.confidence_scores.neutral, document.confidence_scores.negative] for document in doc_result]
    
    return [len([document.sentiment for document in doc_result if document.sentiment == x]) for x in ["positive", "neutral", "negative"]]

#sanitizes the tweets into just text stored in an array
def parse_tweets(tweets):
    return [tweet['text'] for tweet in tweets['data']]

def main():  
   response = input('Please enter a search term or quit to exit: ')
   if(response == 'quit'):
       exit()
   tweets = twitter_client(response)
   client = authenticate_client()
   parsed_tweets = parse_tweets(tweets)
   doc_sentiments = sentiment_analysis(client, parsed_tweets)
   graph_data(doc_sentiments)

if __name__ == "__main__":
    main()