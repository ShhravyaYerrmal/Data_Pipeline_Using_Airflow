import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs

def run_twitter_etl():
    access_key= "877377810184019968-wIYYMmXEASf0sgTxFAY47MB8T4RQ6A7"
    access_secret= "TgqZmYlKWG3A5YBaUfFwTk3v4iYIWxlhwc3Kkyf2G5olA"
    consumer_key= "0hrLAisR6kNkgN6kJqnJ756eF"
    consumer_secret= "7vEw4BEX39FI3182cU66xbIp9chFckeZNeNfFpeZKMXcsLsR3g"

    # Twitter authentication

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # Creating an API object
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name='@elonmusk', 
                                # 200 is the maximum allowed count
                                count=200,
                                include_rts = False,
                                # Necessary to keep full_text 
                                # otherwise only the first 140 words are extracted
                                tweet_mode = 'extended'
                                )
    list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        list.append(refined_tweet)

    df = pd.DataFrame(list)
    df.to_csv('refined_tweets.csv')