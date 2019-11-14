import oauth2
import pandas as pd
import sys
import sqlite3
import json
from config import *
from collections import Counter
from soynlp.tokenizer import MaxScoreTokenizer
from konlpy.tag import *
import platform
import datetime
import re
import numpy as np
from pprint import pprint
import pymysql
import matplotlib.pyplot as plt

dbs = ""

try:
    #데이터베이스 서버 연결
    conf = pymysql.connect(host='106.10.32.85', 
                        user='root',
                        passwd='shsmsrpwhgdktjqjdlqslek!', 
                        db='SPST_S',
                        charset='utf8',
                        port=3306,
                        )
    cursor = conf.cursor()
    dbs = "mysql"
except:
    #데이터베이스 로딩
    if(platform.system()=='Windows'):
    	pathvar = os.path.dirname( os.path.abspath( __file__ ) ).split('\\')[2]
    	conf = sqlite3.connect("C:/Users/"+ pathvar + "/SPST_S.db")
    	cursor = conf.cursor()
    elif(platform.system()=='Darwin'):
    	file = "SPST_S.db"
    	conf = sqlite3.connect(file)
    	cursor = conf.cursor()
    dbs = "sqlite"

print(dbs)

""" 파일 순서 - 1 - 
특정한 아이디에 대한 정보를 가져와(크롤링해) json 파일로 저장합니다. """

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

    fword = [newcount[i][0] for i in range(len(newcount))]
    fnumber = [newcount[i][1] for i in range(len(newcount))]
    fxs = [i for i, _ in enumerate(fword)]
    print(fword,per2)
    return fword,per2


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
        if(data['감정범주'][x] == '기쁨' or data['감정범주'][x] == '  흥미' or data['감정범주'][x] == '놀람'):
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
        emot = '1'
    elif (result_neg > result_pos and result_neg > result_neu):
        emot = '0'
    else:
        emot = '0.5'

    f_pos.close()
    f_neg.close()
    f_neu.close()
    f_test.close()

    return emot

""" 파일 6 """
def profiling(names,key_max,pointlist,iH,fword,per2,emot):
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
        
        plt.bar(fword,per2)
        plt.ylabel("단어 수")
        plt.title("단어 계산")
        plt.xticks([i + 0.5 for i, _ in enumerate(fword)], fword, rotation = 90)
        plt.show()
    if not iH:
        print("관심사 is %s"%(fword[0]))
        print("주제 성향 is %s입니다."%(emots))
        print("Graph is None")
    return user_profile

def interactive(text1):
    global user_profile
    def f1(x):
        return resultk[x]
    userlist = pd.read_sql("SELECT * FROM USER_INFO",conf)
    userlist = list(userlist["ID"])
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
                lenarr2 = len(arr2)

                data = ""
                for x in range(lenarr2):
                    data += arr2[x]
                    iH = isHangul(data)

                parses = datapaser(data) 
                fword,per2 = express(parses)
                pointlist = []
                if iH:
                    reduceword = ['뉴콘','첫공','총막','피켓팅']
                    for x in reduceword:
                        if(fword[0] == x):
                            pointword = '콘서트'
                            pointlist.append(pointword)
                            pointlist.append(int(per2[0]))
                            break
                        else:
                            pointword = fword[0]
                            pointlist.append(pointword)
                            pointlist.append(int(per2[0]))
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
                user_profile = profiling(text1,key_max,pointlist,iH,fword,per2,emot)

                print(user_profile["time"][0],(int(user_profile["time"][0])*3600))
                values = [user_profile["id"][0],str(int(user_profile["time"][0])*3600),user_profile["user_topic"][0],user_profile["emotion"][0]]
                query = """INSERT INTO USER_ANALYSIS (ID, ACTIVE_TIME, SUBJECT, EMOTION) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query,values)
                conf.commit()
                userset = pd.read_sql("SELECT * FROM USER_ANALYSIS",conf)
                cols = list(userset)


myuser = pd.read_sql("SELECT * FROM PERSONAL",conf)
point = myuser["ID"][0]
interactive(point)
