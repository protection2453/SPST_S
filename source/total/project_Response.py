from konlpy.tag import Okt
import os, json
from project_MarkovChain import *
from project_MarkovChain import word_choice, set_word3

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
