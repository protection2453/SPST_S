""" 파일 순서 - 2 - 
가져온 파일을 기반으로 개인정보가 저장될 1차 데이터프레임을 생성하고 
주요 활동 시간을 파악해 저장합니다. """


from personal_json import *
from pprint import pprint
import pandas as pd
from collections import Counter
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import os
from konlpy.tag import *

#matplotlib 그래프 한글 깨짐 방지. 폰트 설정
font_fname = 'C:/Windows/Fonts/NanumGothic.ttf'
font_family = fm.FontProperties(fname=font_fname).get_name()
plt.rcParams["font.family"] = font_family
plt.rcParams['font.size'] = 20.
plt.rcParams['xtick.labelsize'] = 11.
plt.rcParams['ytick.labelsize'] = 11.
plt.rcParams['axes.labelsize'] = 15.

#개인 아이디 크롤링 결과 호출 
main()
with open(names+"_twitter.json",encoding='UTF-8') as json_file:
    json_data = json.load(json_file)
from pprint import pprint

#개인 정보 데이터 셋 저장 
personal_list = [names for x in range(len(json_data))] 
personal_set = pd.DataFrame(personal_list, columns=["id"])
personal_set["user_time"] = [json_data[x]["created_time"] for x in range(len(json_data))]
personal_set["user_message"] = [json_data[x]["message"] for x in range(len(json_data))]
personal_set["uesr_tags"] = [json_data[x]["hashtags"] for x in range(len(json_data))]
personal_set["user_link"] = [json_data[x]["link"] for x in range(len(json_data))]
#pprint(personal_set)

#주로 활동하는 시간 파악
arr = list(personal_set["user_time"])
isarr = [int((((arr[x].split())[1].split(":"))[0])) for x in range(len(arr))]
result = Counter(isarr)
def f1(x):
	return result[x]
key_max = max(result.keys(), key=f1)

#빈도수 바탕 주제 분석 - 형태소 분리
arr2 = list(personal_set["user_message"])
