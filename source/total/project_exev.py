#필요 라이브러리 및 파일 호출
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
import sqlite3
import pandas as pd
import os
import time
import oauth2
import pandas as pd
import json
import datetime
from config import *
import sys
from pprint import pprint
from collections import Counter
from konlpy.tag import *
import numpy as np
import re
from soynlp.tokenizer import MaxScoreTokenizer
from konlpy.tag import Okt
import random
#from PIL import Image

#from project_Response import *
#from personal_json import *
#from personal_data import *
#from personal_topic import *
#from feeling_to_data import *
#from personal_feeling import *
#from personal_profile import *

""" 부가 파일 1 """

dict_file = "MarcovChain-data.json"
dic = {}
okt = Okt()

# 업데이트
def register_dic(words):
    global dic
    if len(words) == 0: return
    tmp = ["@"]
    for i in words:
        word = i[0]
        if word == "" or word == "\r\n" or word == "\n": continue
        tmp.append(word)
        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:]

        set_word3(dic, tmp)

        if word == "." or word == "?":
            tmp = ["@"]
            continue
    # 딕셔너리가 변경될때 저장
    json.dump(dic, open(dict_file, "w", encoding="utf-8"))

def make_sentence(head):
    if not head in dic: return ""
    ret = []

    if head != "@": ret.append(head)
    top = dic[head]

    w1 = word_choice(top)
    w2 = word_choice(top[w1])

    ret.append(w1)
    ret.append(w2)

    while True:
        if w1 in dic and w2 in dic[w1]:
            w3 = word_choice(dic[w1][w2])
        else:
            w3 = ""
        ret.append(w3)
        if w3 == "/" or w3 == "? " or w3 == "": break
        w1, w2 = w2, w3
    ret = " ".join(ret)

    return ret

def make_reply(text):

    # 단어 학습
    if not text[-1] in [".", "?"]: text += "."
    words = okt.pos(text)
    register_dic(words)
    # 사전에 단어가 있다면 그것을 기반으로 문장 만듬
    for word in words:
        face = word[0]
        if face in dic: return make_sentence(face)

    return make_sentence("@")

if os.path.exists(dict_file):
    dic = json.load(open(dict_file, "r"))

""" 부가 파일 2 마르코프 체인"""

# 마르코프 체인 딕셔너리

def make_dic(words):
    tmp = ["@"]
    dic = {}

    for word in words:
        tmp.append(word)

        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:]

        try:
            set_word3(dic, tmp)
        except:
            pass
        if word == ".":
            tmp = ["@"]
            continue

    return dic

# 딕셔너리 등록

def set_word3(dic, s3):
    w1, w2, w3 = s3

    if not w1 in dic: dic[w1] = {}
    if not w2 in dic[w1]: dic[w1][w2] = {}
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0

    dic[w1][w2][w3] += 1

# 문장 만들기

def make_sentence(dic):
    ret = []
    if not '@' in dic: return "no dic"
    top = dic['@']

    w1 = word_choice(top)
    w2 = word_choice(top[w1])

    ret.append(w1)
    ret.append(w2)

    while True:
        w3 = word_choice(dic[w1][w2])
        ret.append(w3)
        if w3 == ".": break
        w1, w2 = w2, w3
    ret = " ".join(ret)

    return ret

def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))

if __name__ == '__main__':
    dict_file = "markov-chain.json"

    sentence = """오늘 콘서트 티켓팅 발매 시작! 우리 꼭 모두 성공해봐요."""

    twitter = Okt()
    malist = twitter.pos(sentence, norm=True)
    words = []


    for word in malist:
        if not word[1] in ["Punctuation"]:
            words.append(word[0])
        if word[0] == '.':
            words.append(word[0])

    dic = make_dic(words)
    pprint(words)
    pprint(dic)

    json.dump(dic, open(dict_file, "w", encoding="utf-8"))

    new_sentence = make_sentence(dic)
    print(new_sentence)


""" 파일 순서 - 1 - 
특정한 아이디에 대한 정보를 가져와(크롤링해) json 파일로 저장합니다. """


import oauth2
import pandas as pd
import json
import datetime
import time
from config import *
import sqlite3
import sys

#[CODE 1]
def oauth2_request(consumer_key, consumer_secret, access_token, access_secret):
    try:
        consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
        token = oauth2.Token(key=access_token, secret=access_secret)
        client = oauth2.Client(consumer, token)
        return client
    except Exception as e:
        print(e)
        return None

#[CODE 2]
def get_user_timeline(client, screen_name, count=50, include_rts='False'):
    base = "https://api.twitter.com/1.1"
    node = "/statuses/user_timeline.json"
    fields = "?screen_name=%s&count=%s&include_rts=%s" % (screen_name, count, include_rts)

    url = base + node + fields

    response, data = client.request(url)

    try:
        if response['status'] == '200':
            return json.loads(data.decode('utf-8'))
    except Exception as e:
        print(e)
        return None

#[CODE 3]
def getTwitterTwit(tweet, jsonResult):

    tweet_id = tweet['id_str']
    tweet_message = '' if 'text' not in tweet.keys() else tweet['text']

    screen_name = '' if 'user' not in tweet.keys() else tweet['user']['screen_name']

    tweet_link = ''
    if tweet['entities']['urls']: #list

        for i, val in enumerate(tweet['entities']['urls']):
            tweet_link = tweet_link + tweet['entities']['urls'][i]['url'] + ' '
    else:
        tweet_link = ''

    hashtags = ''
    if tweet['entities']['hashtags']: #list

        for i, val in enumerate(tweet['entities']['hashtags']):
            hashtags = hashtags + tweet['entities']['hashtags'][i]['text'] + ' '
    else:
        hashtags = ''

    if 'created_at' in tweet.keys():
        # Twitter used UTC Format. EST = UTC + 9(Korean Time) Format ex: Fri Feb 10 03:57:27 +0000 2017

        tweet_published = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        tweet_published = tweet_published + datetime.timedelta(hours=+9)
        tweet_published = tweet_published.strftime('%Y-%m-%d %H:%M:%S')
    else:
        tweet_published = ''

    num_favorite_count = 0 if 'favorite_count' not in tweet.keys() else tweet['favorite_count']
    num_comments = 0
    num_shares = 0 if 'retweet_count' not in tweet.keys() else tweet['retweet_count']
    num_likes = num_favorite_count
    num_loves = num_wows = num_hahas = num_sads = num_angrys = 0

    jsonResult.append({'post_id':tweet_id, 'message':tweet_message,
                    'name':screen_name, 'link':tweet_link,
                    'created_time':tweet_published, 'num_reactions':num_favorite_count,
                    'num_comments':num_comments, 'num_shares':num_shares,
                    'num_likes':num_likes, 'num_loves':num_loves,
                    'num_wows':num_wows, 'num_hahas':num_hahas,
                    'num_sads':num_sads, 'num_angrys':num_angrys, 'hashtags': hashtags})
#main
def main(names):
    screen_name = names
    num_posts = 100
    jsonResult = []

    ck = "oCfme0qMTyYybPUU0ABwKNHKg"
    cs = "1VP4phAtG0Y1ILTe5RGL7XYGHkNrWEzzxv8fk0cWym1p9yfNIO"
    at = "2910321932-RkciOAbw8WYB2nIISDrFSREfbDnxDIydAdX2mLB"
    asc = "faRZmsdWYWQ8mLdYN40qmj7B5eA0Ifl9RglLohzi8fCqa"
    
    client = oauth2_request(ck, cs, at, asc)
    tweets = get_user_timeline(client, screen_name)

    for tweet in tweets:
        getTwitterTwit(tweet, jsonResult)

    with open('%s_twitter.json' % (screen_name), 'w', encoding='utf8') as outfile:
        str_ = json.dumps(jsonResult,
                      indent=4, sort_keys=True,
                      ensure_ascii=False)
        outfile.write(str_)

    print ('%s_twitter.json SAVED' % (screen_name))

""" 파일 순서 - 2 - 
가져온 파일을 기반으로 개인정보가 저장될 1차 데이터프레임을 생성하고 
주요 활동 시간을 파악해 저장합니다. """


from personal_json import *
from pprint import pprint
from collections import Counter
#import matplotlib.font_manager as fm
#import matplotlib.pyplot as plt
import os
from konlpy.tag import *

def f1(x):
    return result[x]

def personal_datas(names):

    #개인 아이디 크롤링 결과 호출 
    #main()
    with open(names+"_twitter.json",encoding='UTF-8') as json_file:
        json_data = json.load(json_file)


    #개인 정보 데이터 셋 저장 
    personal_list = [names for x in range(len(json_data))] 
    personal_set = pd.DataFrame(personal_list, columns=["id"])
    personal_set["user_time"] = [json_data[x]["created_time"] for x in range(len(json_data))]
    personal_set["user_message"] = [json_data[x]["message"] for x in range(len(json_data))]
    personal_set["uesr_tags"] = [json_data[x]["hashtags"] for x in range(len(json_data))]
    personal_set["user_link"] = [json_data[x]["link"] for x in range(len(json_data))]
    #pprint(personal_set)
    
    return personal_set


""" 파일 순서 - 3 - 
주요 활동 시간을 정했다면 다음에 필요한 것은 해당 유저가 관심있어하는 
관심사를 가지고 공격할 주제를 만드는 것입니다. 
관심사는 글의 특정 단어 빈도수로 측정합니다."""


from personal_data import *
import numpy as np
import re
from soynlp.tokenizer import MaxScoreTokenizer

boundmorpheme = ["은", "는", "이", "가", "을", "를", "로써", "에서", "에게서", "부터", "까지", "에게", "한테", "께", "와", "과", "의", "로서", "으로서", "로", "으로"] # 조사
exceptions = boundmorpheme

scores = {'티켓이': 0.3, '티켓': 0.7, '좋아요': 0.2, '좋아':0.5}
tokenizer = MaxScoreTokenizer(scores=scores)

def isHangul(text):
    #Check the Python Version
    pyVer3 =  sys.version_info >= (3, 0)

    if pyVer3 : # for Ver 3 or later
        encText = text
    else: # for Ver 2.x
        if type(text) is not unicode:
            encText = text.decode('utf-8')
        else:
            encText = text

    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
    return hanCount > 0

iH = 0

def bringdata(lenarr2):
    #데이터 가져오기
    data = ""
    for x in range(lenarr2):
        data += arr2[x]
        iH = isHangul(data)
    pprint(iH)
    return data

def datapaser(data):
    #데이터 정제
    parse = re.sub("[^0-9a-zA-Z\\s]+[^ ㄱ - ㅣ 가-힣]", "", data)
    parse = parse.lower().split()
    for x in range(len(parse)):
        parse[x] = re.sub("[^ ㄱ - ㅣ 가-힣]+","",parse[x])
        try:
            ay = tokenizer.tokenize(parse[x])
            if(ay == boundmorpheme):
                pasrs[x] = ""
            else:
                parse[x] = ay
        except:
            parse[x] = re.sub("[^ ㄱ - ㅣ 가-힣]+","",parse[x])
            
    parses = []
    for x in range(len(parse)):
        try:
            parses.append(parse[x][0])
        except:
            continue
    return parses
def express(parses):
    #표현
    counts = Counter(parses)
    counts = counts.most_common()
    length = len(counts)
    newcount = []
    for i in range(length):
        if counts[i][0] not in exceptions:
            newcount.append(counts[i])

    counts_to_frame = pd.DataFrame(counts, columns = ["Word", "Counts"])
    countsum1 = sum(counts_to_frame["Counts"])
    per1 = [(counts_to_frame["Counts"][i]/countsum1) * 100 \
            for i in range(len(counts_to_frame))]
    counts_to_frame["Per"] = np.array(per1)

    new_to_frame = pd.DataFrame(newcount, columns = ["Word", "Counts"])
    countsum2 = sum(new_to_frame["Counts"])
    per2 = [(new_to_frame["Counts"][i]/countsum2) * 100 \
            for i in range(len(new_to_frame))]
    new_to_frame["Per"] = np.array(per2)

    fword = [newcount[i][0] for i in range(len(newcount))][:30]
    fnumber = [newcount[i][1] for i in range(len(newcount))][:30]

    return fword,fnumber

    if iH:
        reduceword = ['뉴콘','첫공','총막','피켓팅']
        for x in reduceword:
            if(fword[0] == x):
                pointword = '콘서트'
            else:
                pointword = fword[0]
        pointlist.append(pointword)
        pointlist.append(fnumber[0])
    else:
        pointlist.append("한글 아님")
        pointlist.append("None")
        fword.append("None")
    fxs = [i for i, _ in enumerate(fword)]
    return pointlist

""" 파일 순서 - 4 - 
아이디와 시간정보, 주제는 파악했습니다.
마지막으로 사용자가 가지는 감정을 파악할 것입니다.
이 파일은 감정 파악을 위한 정보로서 감정사전을 정제하는 과정입니다."""

def exceling():
    data = pd.read_excel('feeling.xlsx')
    posl = []
    navl = []
    natl = []

    for x in range(len(data['단어'])): 
        if(data['감정범주'][x] == '기쁨' or data['감정범주'][x] == ' 흥미' or data['감정범주'][x] == '놀람'):
            posl.append(data['단어'][x])
        if(data['감정범주'][x] == '혐오' or data['감정범주'][x] == '분노' or data['감정범주'][x] == '통증' or data['감정범주'][x] == '지루함' or data['감정범주'][x] == '공포'):
            navl.append(data['단어'][x])
        if(data['감정범주'][x] == '슬픔' or data['감정범주'][x] == '중성' or data['감정범주'][x] == '기타'):
            natl.append(data['단어'][x])

    feels = list(data['감정범주'])
    feels = list(set(feels))

    f = open("positive.txt","w",encoding='utf-8')
    for x in range(len(posl)):
        data = posl[x] + "\n"
        f.write(data)
    f.close()

    f = open("negative.txt","w",encoding='utf-8')
    for x in range(len(navl)):
        data = navl[x]  + "\n"
        f.write(data)
    f.close()

    f = open("neutral.txt","w",encoding='utf-8')
    for x in range(len(natl)):
        data = natl[x] + "\n"
        f.write(data)
    f.close()


""" 파일 순서 - 5 - 
아이디와 시간정보, 주제는 파악했습니다.
마지막으로 사용자가 가지는 감정을 파악할 것입니다.
이 파일은 정제된 감정 사전을 이용해 사용자의 최신글에서 나타나는
감정을 분석합니다."""

emot = ''

list_tag = [u'NNG', u'VV', u'VA', u'VXV', u'UN']
okt = Okt()

#make lists
def getting_list(filename, listname):
    while 1:
        line = filename.readline()
        line_parse = okt.pos(line)
        for i in line_parse:
            if i[1] == u'SW':
                if i[0] in [u'♡', u'♥']:
                    listname.append(i[0])
            if i[1] in list_tag:
                listname.append(i[0])
        if not line:
            break
    return listname
 
#naive bayes classifier + smoothing
def naive_bayes_classifier(test, train, all_count):
    counter = 0
    list_count = []
    for i in test:
        for j in range(len(train)):
            if i == train[j]:
                counter = counter + 1
        list_count.append(counter)
        counter = 0
    list_naive = []
    for i in range(len(list_count)):
        list_naive.append((list_count[i]+1)/float(len(train)+all_count))
    result = 1
    for i in range(len(list_naive)):
        result *= float(round(list_naive[i], 6))
    return float(result)*float(1.0/3.0)

def mainfeel(f_testd):
    global emot
    # get the data
    f_pos = open('positive.txt', 'r',encoding='UTF-8')
    f_neg = open('negative.txt', 'r',encoding='UTF-8')
    f_neu = open('neutral.txt', 'r',encoding='UTF-8')
    f_test = f_testd
     
    # tag list (보통명사, 동사, 형용사, 보조동사, 명사추정범주) 
    # 참고 : https://docs.google.com/spreadsheets/d/1OGAjUvalBuX-oZvZ_-9tEfYD2gQe7hTGsgUpiiBSXI8/edit#gid=0

    list_positive=[]
    list_negative=[]
    list_neutral=[]
     
    # extract test sentence
    test_line = f_test.readline()   
    test_list = okt.pos(test_line)
    test_output=[]
    for i in test_list:
        if (i[1] == u'SW'):
            if (i[0] in [u'♡', u'♥']):
                test_output.append(i[0])
        if (i[1] in list_tag):
            test_output.append(i[0])
     
    # getting_list함수를 통해 필요한 tag를 추출하여 list 생성
    list_positive = getting_list(f_pos, list_positive)
    list_negative = getting_list(f_neg, list_negative)
    list_neutral = getting_list(f_neu, list_neutral)
     
    ALL = len(set(list_positive))+len(set(list_negative))+len(set(list_neutral)) #전체 카운트, 함수에 들어가야한다. (all_count)
    print(ALL)

    # naive bayes 값 계산
    result_pos = naive_bayes_classifier(test_output, list_positive, ALL)
    result_neg = naive_bayes_classifier(test_output, list_negative, ALL)
    result_neu = naive_bayes_classifier(test_output, list_neutral, ALL)
     
    if (result_pos > result_neg and result_pos > result_neu):
        #print('긍정')
        emot = '긍정'
    elif (result_neg > result_pos and result_neg > result_neu):
        #print ('부정')
        emot = '부정'
    else:
        #print ('중립')
        emot = '중립'
     
    '''
    pprint(result_pos)
    pprint(result_neg)
    pprint(result_neu)'''

    f_pos.close()
    f_neg.close()
    f_neu.close()
    f_test.close()

    return emot

""" 파일 순서 - 6 - 
메인 코드입니다. 이 파일을 실행하면 다른 파일들이 모두 실행되며 실행된
결과를 이 파일로 반환합니다. 이 파일은 분석 완료된 결과를 알려줍니다.
아이디, 주요 활동시간, 관심사, 감정의 네 가지가 저장되어 있습니다."""

import pandas as pd
def profiling(names,key_max,pointlist,iH,fword,emot):
    #크롤링 분석 완료
    user_profile = [names]
    user_profile = pd.DataFrame(user_profile, columns=["id"])

    user_profile["time"] = str(key_max)
    user_profile["user_topic"] = pointlist[0]
    user_profile['emotion'] = emot

    #pprint(user_profile)
    print("%s님이 매체를 주로 이용하는 시각은 %d시 입니다."%(names, key_max))

    if iH:
        print("%s님의 관심사는 본문에서 %s번 빈도가 나타난 \"%s\"입니다."%(names, pointlist[1], fword[0]))
        print("%s님이 주제에 대해 주로 나타내는 성향은 %s입니다."%(names, emot))
        '''
        plt.bar(fxs, fnumber)
        plt.ylabel("단어 수")
        plt.title("단어 계산")
        plt.xticks([i + 0.5 for i, _ in enumerate(fword)], fword, rotation = 90)
        plt.show() '''
    if not iH:
        print("관심사 is %s"%(fword[0]))
        print("주제 성향 is %s입니다."%(emots))
        print("Graph is None")
    return user_profile


"""파일 7 메인 """
pathvar = os.path.dirname( os.path.abspath( __file__ ) ).split('\\')[2]

#데이터베이스 생성
if os.path.isfile("C:/Users/"+ pathvar + "/Users.db"):
  print ("해당 파일이 있습니다. 데이터베이스를 불러옵니다.")
  conf = sqlite3.connect("C:/Users/"+ pathvar + "/Users.db")
  cursor = conf.cursor()
  userset = pd.read_sql("SELECT * FROM user_info",conf)
  userlist = pd.read_sql("SELECT * FROM user_info",conf)
  userlist = list(userlist["id"])
  cols = list(userset)
  print (userset)
else:
  print ("그런 이름의 파일은 없습니다. 새 데이터베이스를 생성합니다.")
  conf = sqlite3.connect("C:/Users/"+ pathvar + "/Users.db")
  cursor = conf.cursor() 
  cursor.execute('create table user_info(id, name, address)')
  cursor.execute('create table user_analysis(id, active_time, subject, emotion)')
  userset = pd.read_sql("SELECT * FROM user_info",conf)
  userlist = pd.read_sql("SELECT * FROM user_info",conf)
  userlist = list(userlist["id"])
  cols = list(userset)

ids = userset["id"].tolist()
nas = userset["name"].tolist()
ads = userset["address"].tolist()

lists = []
for x in range(len(ids)):
    lists.append(tuple(ids[x]))

#결과 저장 - 추가
def more(text1,text2,text3):
    text1 = text1.replace(" ","") #공백은 결과 저장 버튼을 눌러도 저장되지 않습니다.
    text2 = text2.replace(" ","")
    text3 = text3.replace(" ","")

    values = [text1,text2,text3]
    if(len(values[0]) != 0 and len(values[1]) != 0 and len(values[2]) != 0):
        cursor.execute("insert into user_info values (?,?,?)",values)
        conf.commit()
        userset = pd.read_sql("SELECT * FROM user_info",conf)
        cols = list(userset)

#결과 저장 - 제거
def grep(text1,text2,text3):
    text1 = text1.replace(" ","") #공백은 결과 저장 버튼을 눌러도 저장되지 않습니다.
    text2 = text2.replace(" ","")
    text3 = text3.replace(" ","")

    values = [text1,text2,text3]
    print(type(text1))
    if(len(values[0]) != 0 and len(values[1]) != 0 and len(values[2]) != 0):
        query = "DELETE FROM 'user_info' where id =" + "'" + text1 + "'" + "and name =" + "'" + text2 + "'" + "and address =" + "'" + text3 + "'"
        cursor.execute(query)
        conf.commit()
        userset = pd.read_sql("SELECT * FROM user_info",conf)
        cols = list(userset)

#실수 종료 방지
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"): 
        root.destroy()

#사원 테이블 호출
def my_table(self):
    treeview.tag_configure("tag2", background="red")

#창 숨기기
def hide():
    root.withdraw()

#사원 관리
class MyFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=True)

        #id
        frame1 = Frame(self)
        frame1.pack(fill=X)
        lblId = Label(frame1, text ="아이디",width=10)
        lblId.pack(side=LEFT,padx=10,pady=10)
        entryId = Entry(frame1)
        entryId.pack(fill=X, padx=10, expand=True)

        #성명
        frame2 = Frame(self)
        frame2.pack(fill=X)
        lblName = Label(frame2, text ="성명",width=10)
        lblName.pack(side=LEFT,padx=10,pady=10)
        entryName = Entry(frame2)
        entryName.pack(fill=X, padx=10, expand=True)

        #부서
        frame3 = Frame(self)
        frame3.pack(fill=X)
        lblDepart = Label(frame3, text ="부서",width=10)
        lblDepart.pack(side=LEFT,padx=10,pady=10)
        entryDepart = Entry(frame3)
        entryDepart.pack(fill=X, padx=10, expand=True)

        #저장
        frame4 = Frame(self)
        frame4.pack(fill=X)
        btnSave = Button(frame4, text="사원추가",command=lambda:more(entryId.get(),entryName.get(),entryDepart.get()))
        btnSave.pack(side=RIGHT, padx=10, pady=10)

        frame5 = Frame(self)
        frame5.pack(fill=X)
        btnDel = Button(frame5, text="사원제거",command=lambda:grep(entryId.get(),entryName.get(),entryDepart.get()))
        btnDel.pack(side=RIGHT, padx=10, pady=10)

        frame6 = Frame(self)
        frame6.place(x=30, y = 440)
        btnhid = Button(frame6, text="돌아가기",command=hide)
        btnhid.place(x=30, y = 440)

#사원 관리 메인
def employee_manage():
    global x0, y0,hides
    emplo = Toplevel(root)
    emplo.resizable(0, 0)
    emplo.title("사원 관리")
    width2,height2 = x0+20,y0+30
    screen2_wid = root.winfo_screenwidth()
    screen2_hei = root.winfo_screenheight()
    x2 = ((screen2_wid/2) - (width2/2))
    y2 = (screen2_hei/2) - (height2/2)
    emplo.geometry('%dx%d+%d+%d' % (width2, height2, x2, y2))

    userset = pd.read_sql("SELECT * FROM user_info",conf)
    cols = list(userset)
    ids = userset["id"].tolist()
    nas = userset["name"].tolist()
    ads = userset["address"].tolist()

    e_lbl = Label(emplo,text="사원 목록 테이블")
    e_lbl.pack()
    e_but = Label(emplo,text="My_Table")
    e_but.pack()

    treelists = []
    for x in range(len(ids)):
        treelist = []
        treelist.append(ids[x])
        treelist.append(nas[x])
        treelist.append(ads[x])
        treelists.append(tuple(treelist))
    #print(treelists)

    treeview=tkinter.ttk.Treeview(emplo, columns=["one", "two","three"])
    treeview.column("#0", width=50)
    treeview.heading("#0",text="num") #index
    treeview.column("one", width=70)
    treeview.heading("one", text=cols[0]) #id
    treeview.column("two", width=50)
    treeview.heading("two", text=cols[1], anchor="center") #name
    treeview.column("three", width=100, anchor="w")
    treeview.heading("three", text=cols[2], anchor="center") #address

    for i in range(len(treelists)):
        treeview.insert('', 'end', text=i, values=treelists[i], iid=str(i)+"번")

    treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=my_table)
    treeview.pack(side=TOP,fill=X)

    app = MyFrame(emplo)
    emplo.mainloop()


user_profile = 0

#분석 시작
def interactive(text1):
    global user_profile
    def f1(x):
        return resultk[x]

    userlist = pd.read_sql("SELECT * FROM user_info",conf)
    userlist = list(userlist["id"])

    text1 = text1.replace(" ","")
    if(len(text1) != 0):
        for user in userlist:
            if(text1 == user):
                #try:
                main(text1)
                personal_set = (personal_datas(text1))
                #주로 활동하는 시간 파악
                arrs = list(personal_set["user_time"])
                isarr = [int((((arrs[x].split())[1].split(":"))[0])) for x in range(len(arrs))]
                resultk = Counter(isarr)
                key_max = max(resultk.keys(), key=f1)

                #빈도수 바탕 주제 분석 - 형태소 분리
                arr2 = list(personal_set["user_message"])
                #print(arr2)
                lenarr2 = len(arr2)

                data = ""
                for x in range(lenarr2):
                    data += arr2[x]
                    iH = isHangul(data)

                parses = datapaser(data) 
                fword,fnumber = express(parses)
                pointlist = []
                if iH:
                    reduceword = ['뉴콘']
                    for x in reduceword:
                        if(fword[0] == x):
                            pointword = '콘서트'
                        else:
                            pointword = fword[0]
                            pointlist.append(pointword)
                            pointlist.append(fnumber[0])
                else:
                    pointlist.append("한글 아님")
                    pointlist.append("None")
                    fword.append("None")
                fxs = [i for i, _ in enumerate(fword)]
                exceling()
                #빈도수 바탕 주제 분석 - 감정 분석 밑바탕 파일
                f = open("train_docs.txt","w",encoding='utf-8')
                data = arr2[0]
                pprint(arr2[0])
                f.write(str(data))
                f.close()

                f_test = open('train_docs.txt','r',encoding='UTF-8')
                emot = mainfeel(f_test)
                user_profile = profiling(text1,key_max,pointlist,iH,fword,emot)
                analy_result(user_profile)

                values = [user_profile["id"][0],user_profile["time"][0],user_profile["user_topic"][0],user_profile["emotion"][0]]
                cursor.execute("insert into user_analysis values (?,?,?,?)",values)
                conf.commit()
                userset = pd.read_sql("SELECT * FROM user_analysis",conf)
                cols = list(userset)

                #except Exception as ex:
                #    print("None information",ex)
    else:
        messagebox.showinfo(title="Web Crawlling",message="입력 후 버튼을 눌러주세요.")

#훈련 결과
def analy_result(userdata):
    print(userdata)
    print(userdata["user_topic"][0])
    messagebox.showinfo(title='Deep Learning', message=show_newMessage(userdata["user_topic"][0]))

def show_newMessage(topicdata):
    changelist = ['콘서트','공연장','스포츠','공연','표','암표','재관','티켓팅']
    for x in changelist:
        if(x == topicdata):
            topicdata = 티켓
            message = topicdata+" "+"구하는법"

    message = "티켓 구하는법"
    return make_reply(message)

    message = ""
    new_message = make_reply(message)

#훈련 관리
class MyFrames(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=True)

        #목록
        frame1 = Frame(self)
        frame1.pack(fill=X)
        IblLi = Label(frame1, text="사원 목록: "+str(userlist))
        IblLi.pack()

        #id
        frame2 = Frame(self)
        frame2.pack(fill=X)
        lblId = Label(frame2, text ="분석할 아이디",width=10)
        lblId.pack(side=LEFT,padx=10,pady=10)
        entryId = Entry(frame2)
        entryId.pack(fill=X, padx=10, expand=True)

        #훈련
        frame3 = Frame(self)
        frame3.pack(fill=X)
        btanaly = Button(frame3, text="훈련 시작",command=lambda:interactive(entryId.get()))
        btanaly.pack(side=RIGHT, padx=10,pady=10)

#훈련 관리 메인
def analysis_manage():
    global x0, y0
    analys = Toplevel(root)
    analys.resizable(0, 0)
    analys.title("훈련 관리")
    width3,height3 = x0+20,y0+30
    screen3_wid = root.winfo_screenwidth()
    screen3_hei = root.winfo_screenheight()
    x3 = ((screen3_wid/2) - (width3/2))
    y3 = (screen3_hei/2) - (height3/2)
    analys.geometry('%dx%d+%d+%d' % (width3, height3, x3, y3))

    userlist = pd.read_sql("SELECT * FROM user_info",conf)
    userlist = list(userlist["id"])

    userset = pd.read_sql("SELECT * FROM user_analysis",conf)
    cols = list(userset)

    ids = userset["id"].tolist()
    ats = userset["active_time"].tolist()
    sus = userset["subject"].tolist()
    ems = userset["emotion"].tolist()

    e_lbl = Label(analys,text="훈련 관리 테이블")
    e_lbl.pack()
    e_but = Label(analys,text="My_Table")
    e_but.pack()

    treeview=tkinter.ttk.Treeview(analys, columns=["one", "two","three","four"])
    treeview.column("#0", width=50)
    treeview.heading("#0",text="num") #index
    treeview.column("one", width=70,anchor="w")
    treeview.heading("one", text=cols[0],anchor="center") #id
    treeview.column("two", width=50,anchor="w")
    treeview.heading("two", text=cols[1],anchor="center") #active time
    treeview.column("three", width=100,anchor="w")
    treeview.heading("three", text=cols[2],anchor="center") #subject
    treeview.column("four", width=100, anchor="w")
    treeview.heading("four", text=cols[3], anchor="center") #emotion

    treelists = []
    for x in range(len(ids)):
        treelist = []
        treelist.append(ids[x])
        treelist.append(ats[x])
        treelist.append(sus[x])
        treelist.append(ems[x])
        treelists.append(tuple(treelist))

    for i in range(len(treelists)):
        treeview.insert('', 'end', text=i, values=treelists[i], iid=str(i)+"번")

    treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=my_table)
    treeview.pack(side=TOP,fill=X)

    app = MyFrames(analys)
    analys.mainloop()

#메인 화면
def center_window(width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

root = Tk()
root.resizable(0, 0)
x0, y0 = 820, 490
center_window(x0, y0)
root.title("메인 화면")
root.iconbitmap(default=r'C:/Users/' + pathvar + '/Downloads/SPST_S-master/project_icon.ico')

'''image = Image.open("logo.gif") #창 크기에 맞게 이미지 크기 조절
resize_image = image.resize((x0,y0))
resize_image.save('logo.gif') '''
images = PhotoImage(file = "logo.gif") #이미지 배치
lbl = Label(root, image=images)
lbl.pack(side="bottom",fill="both",expand="True")

btn1 = Button(root, text="사원관리", command=employee_manage)
btn1.place(x=700, y = 400)

btn = Button(root, text="훈련관리", command=analysis_manage)
btn.place(x=700, y = 440)

Button(root, text="종   료", command=on_closing).place(x=30, y = 440)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
