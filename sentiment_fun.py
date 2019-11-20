# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 18:59:13 2019

@author: Admin
"""

import tweepy
import textblob
import pandas as pd

consumer_key  = "QHdoSPNYZdSrH2SITinjXH7B1"
consumer_secret = "FbN8B5FtrwRjdJvm0lZpHwFITC6JLfkDNqlDkKpkpiVAJqX0jI"


access_token = "428768497-5PaJi8GvUSqyHkOb6wA6NM4MVECQstWlLpzTWHIC"
access_token_secret ="wOLACcTCYchHJOBs1P9UaxDaucSHUaJyapa9OJhMVuGuE" 


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
api = tweepy.API(auth)

public_tweets = api.search('bike',count=2,lang='en')
for tweets in public_tweets:
    
    print("\n\nNew Tweet\n\n")
    print(tweets.created_at)
    print(tweets.user.location)
    print(tweets.user.name)
    print()

    analysis = textblob.TextBlob(tweets.text)
    '''
    lan = analysis.detect_language()
    if(lan != 'en'):
        tran = analysis.translate(to='en')
        print("Changed")
        print(tran)
        analysis = tran
    #print(analysis.detect_language())
    '''
    print(analysis.sentiment)
    df = pd.DataFrame(data=[tweet.text for tweet in public_tweets], columns=['Tweets'])

    
   # print(analysis.sentiment)