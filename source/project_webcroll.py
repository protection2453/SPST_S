from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import parse
import tweepy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

keyword = ['아이돌','여자친구','방탄소년단','엑소','트와이스','하스스톤','백현']
results = []
for x in range(len(keyword)):
    point = parse.quote(keyword[x])
    results.append("https://twitter.com/search?q="+point+"&src=typed_query&lang=ko")
    print(results[x],end="\n")

print("\n")
urlp = results[1]
print(urlp,"\n")

html = urlopen(urlp)
bsObj = BeautifulSoup(html.read(),"html.parser")
#print(bsObj.body)

#키를 바탕으로 트위터 데이터 수집
consumer_key = "oCfme0qMTyYybPUU0ABwKNHKg"
consumer_secret = "1VP4phAtG0Y1ILTe5RGL7XYGHkNrWEzzxv8fk0cWym1p9yfNIO"
access_token = "2910321932-RkciOAbw8WYB2nIISDrFSREfbDnxDIydAdX2mLB"
access_token_secret = "faRZmsdWYWQ8mLdYN40qmj7B5eA0Ifl9RglLohzi8fCqa"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret) 
api = tweepy.API(auth) 

results = []

for tweet in tweepy.Cursor(api.search, q=keyword[5], count=100).items():
    results.append(tweet)
    
print(len(results))
#print(results[0])

def process_results(results):
    id_list = [tweet.id for tweet in results]
    data_set = pd.DataFrame(id_list, columns=["id"])

    # Processing Tweet Data
    data_set["text"] = [tweet.text for tweet in results]
    data_set["created_at"] = [tweet.created_at for tweet in results]
    data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
    data_set["favorite_count"] = [tweet.favorite_count for tweet in results]
    data_set["source"] = [tweet.source for tweet in results]

    # Processing User Data
    data_set["user_id"] = [tweet.author.id for tweet in results]
    data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
    data_set["user_name"] = [tweet.author.name for tweet in results]
    data_set["user_created_at"] = [tweet.author.created_at for tweet in results]
    data_set["user_description"] = [tweet.author.description for tweet in results]
    data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
    data_set["user_friends_count"] = [tweet.author.friends_count for tweet in results]
    data_set["user_location"] = [tweet.author.location for tweet in results]

    return data_set

data_set = process_results(results)
print(data_set.head(30))
