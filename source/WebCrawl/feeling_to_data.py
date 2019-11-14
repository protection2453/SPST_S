""" 파일 순서 - 4 - 
아이디와 시간정보, 주제는 파악했습니다.
마지막으로 사용자가 가지는 감정을 파악할 것입니다.
이 파일은 감정 파악을 위한 정보로서 감정사전을 정제하는 과정입니다."""


import pandas as pd
from pprint import pprint

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
