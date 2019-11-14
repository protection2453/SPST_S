import sqlite3
import platform
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
import pandas as pd
import pymysql
from konlpy.tag import Okt
import os, json, random
from pprint import pprint

dbs = ""

try:
    #데이터베이스 서버 연결
    conf = pymysql.connect(host='106.10.32.85', 
                        user='root', 
                        passwd='shsmsrpwhgdktjqjdlqslek!', 
                        db='SPST_S',
                        charset='utf8',
                        port=3306,
                        use_unicode=True)
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
cursor.execute("set names utf8")


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
    #pprint(words)
    #pprint(dic)

    json.dump(dic, open(dict_file, "w", encoding="utf-8"))

    new_sentence = make_sentence(dic)

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
    #if not text[-1] in [".", "?"]: text += "."
    words = okt.pos(text)
    register_dic(words)
    # 사전에 단어가 있다면 그것을 기반으로 문장 만듬
    for word in words:
        face = word[0]
        if face in dic: return make_sentence(face)

    return make_sentence("@")


if os.path.exists(dict_file):
    dic = json.load(open(dict_file, "r"))

myuser = pd.read_sql("SELECT * FROM PERSONAL",conf)
point = myuser["ID"][0]

if __name__ == "__main__":
	userseta = pd.read_sql("SELECT * FROM USER_ANALYSIS where ID=" + "'" + point + "'",conf)
	userseti = pd.read_sql("SELECT * FROM USER_INFO where ID=" + "'" + point + "'",conf)

	name = userseti["NAME"][0]

	subjec = userseta["SUBJECT"][0]
	if(subjec == "콘서트" or subjec == "티켓" or subjec == "티켓팅"):
		message = "티켓 구하는법"
	else:
		message = "티켓 구하는 법"
	new_message = make_reply(message)
	print(new_message)

	
	values = [point,name,new_message]
	query = """INSERT INTO USER_RESULT (ID, NAME, SENTENCE) VALUES (%s, %s, %s)"""
	cursor.execute(query,values)
	conf.commit()
