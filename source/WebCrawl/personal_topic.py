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

#데이터 가져오기
data = ""
for x in range(len(arr2)):
	data += arr2[x]
	iH = isHangul(data)
pprint(iH)

#데이터 정제
parse = re.sub("[^0-9a-zA-Z\\s]+[^ ㄱ - ㅣ 가-힣]", "", data)
parse = parse.lower().split()
#print(parse)
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

pointlist = []
fword = [newcount[i][0] for i in range(len(newcount))][:30]
fnumber = [newcount[i][1] for i in range(len(newcount))][:30]

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
