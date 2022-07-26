from matplotlib.axes import Axes
from matplotlib import pyplot as plt
import numpy as np

import tweepy
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from dotenv import load_dotenv
import os
from os.path import join, dirname

load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY= os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
endpoint = os.getenv('endpoint')
ta_credential = os.getenv('ta_credential')
key = os.getenv('key')

def twitter_client(response):
    search_term = response
    client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY, consumer_secret=API_SECRET_KEY, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET, return_type=dict, wait_on_rate_limit=False)
    return client.search_recent_tweets(f'{search_term} lang:en -is:retweet')

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client
        
def parse_tweets(tweets):
    return [tweet['text'] for tweet in tweets['data']]

def main():  
   response = input('Please enter a search term or quit to exit: ')
   if(response == 'quit'):
       exit()
   tweets = twitter_client(response)
   client = authenticate_client()
   parsed_tweets = parse_tweets(tweets)

if __name__ == "__main__":
    main()