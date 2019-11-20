# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 06:19:16 2019

@author: Admin
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import pandas as pd
import csv
import re #regular expression
from textblob import TextBlob
import string
import textblob
import tweepy
from tweepy import API 
from tweepy import Cursor



class TwitterClient():
    def __init__(self):
        self.auth = Twitter_Authenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
            tweets.append(tweet)
        return tweets

class Twitter_Authenticator():
    def authenticate_twitter_app(self):
        consumer_key  = "QHdoSPNYZdSrH2SITinjXH7B1"
        consumer_secret = "FbN8B5FtrwRjdJvm0lZpHwFITC6JLfkDNqlDkKpkpiVAJqX0jI"
        
        
        access_token = "428768497-5PaJi8GvUSqyHkOb6wA6NM4MVECQstWlLpzTWHIC"
        access_token_secret ="wOLACcTCYchHJOBs1P9UaxDaucSHUaJyapa9OJhMVuGuE" 
        
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
        


class Twitter_Stream():
    
    def __init__(self):
        self.twitter_autenticator = Twitter_Authenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag)
        

class TwitterListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)
        
        
if __name__ == "__main___":
    hash_tag_list = ["bike"]
    fetched_tweets_filename = "tweets.txt"

    twitter_streamer = Twitter_Stream()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    
    twitter_client = TwitterClient()
    print(twitter_client.get_user_timeline_tweets(1))