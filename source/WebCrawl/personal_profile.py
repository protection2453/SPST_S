""" 파일 순서 - 6 - 
메인 코드입니다. 이 파일을 실행하면 다른 파일들이 모두 실행되며 실행된
결과를 이 파일로 반환합니다. 이 파일은 분석 완료된 결과를 알려줍니다.
아이디, 주요 활동시간, 관심사, 감정의 네 가지가 저장되어 있습니다."""


from personal_feeling import *
from personal_topic import *

if(emot == 'pos'):
	emots = '긍정'
elif(emot == 'neg'):
	emots = '부정'
elif(emot == 'nat'):
	emots = '중립'
else:
	emots = 'None'

#크롤링 분석 완료
user_profile = [names]
user_profile = pd.DataFrame(user_profile, columns=["id"])

user_profile["time"] = str(key_max)
user_profile["user_topic"] = pointlist[0]
user_profile['emotion'] = emot

pprint(user_profile)
print("%s님이 매체를 주로 이용하는 시각은 %d시 입니다."%(names, key_max))

if iH:
	print("%s님의 관심사는 본문에서 %s번 빈도가 나타난 \"%s\"입니다."%(names, pointlist[1], fword[0]))
	print("%s님이 주제에 대해 주로 나타내는 성향은 %s입니다."%(names, emots))
	plt.bar(fxs, fnumber)
	plt.ylabel("단어 수")
	plt.title("단어 계산")
	plt.xticks([i + 0.5 for i, _ in enumerate(fword)], fword, rotation = 90)
	plt.show()
if not iH:
	print("관심사 is %s"%(fword[0]))
	print("주제 성향 is %s입니다."%(emots))
	print("Graph is None")
