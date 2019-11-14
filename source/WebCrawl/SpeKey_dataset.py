import tweepy
import pandas as pd
import time
import sqlite3

consumer_key = "oCfme0qMTyYybPUU0ABwKNHKg"
consumer_secret = "1VP4phAtG0Y1ILTe5RGL7XYGHkNrWEzzxv8fk0cWym1p9yfNIO"
access_token = "2910321932-RkciOAbw8WYB2nIISDrFSREfbDnxDIydAdX2mLB"
access_token_secret = "faRZmsdWYWQ8mLdYN40qmj7B5eA0Ifl9RglLohzi8fCqa"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret) 
api = tweepy.API(auth, wait_on_rate_limit=True)

keyword = '콘서트'

results = []
ap = results.append
uy = float(1000)

print("Make Crawling Dataset")
for tweet in tweepy.Cursor(api.search, q=keyword, count=100).items():
    if(len(results)<uy):
        ap(tweet)
        if(len(results)%100==0):
            print("...............%.2f%%"%(len(results)/uy*100.0),end="\n")
    else:
        break

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
rtwi = [] #rtwl = retweet id
rtwh = [] #rtwi = retweet id websiteurl go
ap = rtwi.append
aph = rtwh.append

def retwidadd():
    ke = list(data_set['text'])
    for x in range(len(ke)):
        try:
            kel = ke[x].split()
            kel = kel[1].split(':')
            kel = kel[0]
            if(list(kel)[0]=='@'):
                ap(kel)
                aph("https://twitter.com/"+kel)
            else:
                ap(0)
                aph(0)
        except:
            print("\n")
            print("이상한 경우")
            ke = list(data_set['text'])
            print(ke[x],x)
        #print(rtwi[x],x)
    data_set["rtwi"] = rtwi
    data_set["rtwih"] = rtwh
    #del data_set["Unnamed: 0"]

def to_excel():
    data_set = process_results(results)
    writer = pd.ExcelWriter('multi_df_to_excel.xlsx')
    data_set.to_excel(writer,sheet_name='x')
    writer.save()


retwidadd()

print("\n")

point = 0
con = sqlite3.connect("C:/Users/dsz08/kospi.db") #임의의 DB 생성
data_set.to_sql("crawli"+str(point),con) #해당 데이터베이스에 crawli 테이블로 데이터프레임 추가
cursor = con.cursor() #커서 위치
try:
    df = pd.read_sql("SELECT * FROM crawli"+str(point),con,index_col=None) #데이터베이스에서 불러오기
except:
    point += 1
    df = pd.read_sql("SELECT * FROM crawli"+str(point),con,index_col=None)
