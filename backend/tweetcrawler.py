import tweepy
import sys
from textwrap import TextWrapper
from textblob import TextBlob
from datetime import datetime
from elasticsearch import Elasticsearch
from yaml import load


class TwitterCrawler(object):

    def __init__(self, name):
        self.name = name
        self.keywords = ConfigFile.keywords(self.name)
        self.config_path = '.'

    def connect(self):
        config_dic = open('%s/keywords.yml' % self.config_path, "r")
        config_dic = config_dic.read()
        config_dic = yaml.load(config_dic)
        self.keywords = config_dic.get('twitter_auth')
        consumer_key = config_dic.get(self.name)
        consumer_secret = config_dic.get(self.name)

        access_token = config_dic.get(self.name)
        access_token_secret = config_dic.get(self.name)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return auth

    def crawl(self):
        auth = self.connect()
        streamer = tweepy.Stream(auth=auth, 
                                 listener=StreamListener(), 
                                 timeout=300000000 )
        streamer.filter(None,self.keywords)


class ConfigFile(object):

    def __init__(self, name):
        self.name = name
        self.config_path = '.'
        config_dic = open('%s/keywords.yml' % self.config_path, "r")
        config_dic = config_dic.read()
        config_dic = yaml.load(config_dic)
        self.keywords = config_dic.get(self.name)


class StreamListener(tweepy.StreamListener):

    def __init__(self):
        status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
        es = Elasticsearch()

    def on_status(self, status):
        try:
            print '\n%s %s' % (status.author.screen_name, status.created_at)
            print status.text

            tweet = TextBlob(status.text)

            es.create(index="hpq", 
                      doc_type="tweet", 
                      body={ "author": status.author.screen_name,
                             "date": status.created_at,
                             "message": status.text,
                             "polarity": tweet.sentiment.polarity,
                             "subjectivity": tweet.sentiment.subjectivity }
                     )


        except Exception, e:
            pass

