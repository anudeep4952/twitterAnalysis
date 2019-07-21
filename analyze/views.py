import re

from django.shortcuts import render
import pandas as pd
import numpy as np
from textblob import TextBlob
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor

from twitter import *


from analyze import twitter_credentials


class TweetAnalyzer():
    '''
    functionalit for analyzing and categorizing content from tweets.
    '''

    def clean_tweet(self,tweet):
        x= ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        return x
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        return analysis.sentiment.polarity


    def tweets_to_data_frame(self,tweets):
        df=pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['tweets'])
        '''df['id']=np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
'''
        return df


tweet_analyzer = TweetAnalyzer()

class TwitterClient():
    def __init__(self,twitter_user=None):
       self.auth=TwitterAuthenicator().authenicate_twitter_app()
       self.twitter_client=API(self.auth)
       self.twitter_user=twitter_user

    def get_twitter_client_api(self):
        return  self.twitter_client

    def profile(self):
        return self.twitter_

    def get_user_timeline_tweets(self,num_tweets):
        tweets=[]
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
       # print(len(tweets))
        return tweets
class TwitterAuthenicator():
    def authenicate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


def analyze(request):
 a="https://previews.123rf.com/images/helmut1979/helmut19791507/helmut1979150700021/42500483-x-illustration-cross-of-red-lines-in-paint-style-strokes-.jpg"
 if request.method == 'POST':
     twitter_client = TwitterClient()
     api = twitter_client.get_twitter_client_api()
     h = request.POST.get('userid')
     a = "user not verified "
     twitter = Twitter(auth=OAuth(twitter_credentials.ACCESS_TOKEN,
                                  twitter_credentials.ACCESS_TOKEN_SECRET,
                                  twitter_credentials.CONSUMER_KEY,
                                  twitter_credentials.CONSUMER_SECRET))
     results = twitter.users.search(q=h)
     if not results:
         pic="https://cdn.pixabay.com/photo/2017/07/18/23/23/user-2517433_960_720.png"
         name="no user found"
     else:
         user = results[0]
         name = user["name"]
         pic = str(user["profile_image_url_https"])
         pic = pic.replace('_normal', '')
         verif=user["verified"]

         if verif :
             a="verified user"
         else:
             a="not verified user"

     try:
      tweets = api.user_timeline(screen_name=h, count=20)
      df = tweet_analyzer.tweets_to_data_frame(tweets)
      df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
      df['text'] = np.array([tweet_analyzer.clean_tweet(tweet) for tweet in df['tweets']])

      #score = df['sentiment'].value_counts().idxmax()
      score=df['sentiment'].values.tolist()
      x=dict()
      n=len(score)
      x["pos"]=round((len([i for i in  score if i > 0])/n)*100,2)
      x["neu"]=round((len([i for i in  score if i == 0])/n)*100,2)
      x["neg"]=round((len([i for i in  score if i < 0])/n)*100,2)
      x["summ"]=round((sum(score)/n)*100,2)

     except :
         x=dict()
         return render(request, 'analyze/analyze.html', {'p': pic,'name':name,'verif':a,'x':x})


     p = pic
     return render(request, 'analyze/analyze.html', {'p': pic,'name':name,'verif':a,'x':x})





 else:
     p="https://cdn.pixabay.com/photo/2017/07/18/23/23/user-2517433_960_720.png"
     a="user"
     return render(request,'analyze/analyze.html',{'p':p,'verif':a})

     # print(df[['text', 'sentiment']])


