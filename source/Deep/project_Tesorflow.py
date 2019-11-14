
from collections import Counter
import re
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
import codecs



utf8_f = codecs.open("dataM.txt", 'r', encoding = 'ISO-8859-1')

data = utf8_f.read()
parse = re.sub("[^0-9a-zA-Z\\s]+[^ ㄱ - ㅣ 가-힣]", "", data) # 특수문자 제거
parse = parse.lower().split()

counts = Counter(parse)
counts = counts.most_common()

# 이 부분 한글 인코딩 안되므로 인코딩 해결 시 처리
boundmorpheme = ["은", "는", "이", "가", "을", "를", "로써", "에서", "에게서", "부터", "까지", "에게", "한테", "께", "와", "과", "의", "로서", "으로서", "로", "으로"] # 조사
# 인코딩이랑 한글 형태소 분할해서 자료조사좀 하자

#boundmorpheme = ["a", "the", "an", "for", "and" , "nor", "but", "or", "yey", "so", "i", "we", "me", "us", "some", "how", "just"]

exceptions = boundmorpheme

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

print(new_to_frame)
print("""예외된 단어 30개 :""", new_to_frame[:30])

#한글 깨짐 오류 해결 - 폰트 재정의
plt.rcParams["font.family"] = 'NanumBarunGothic'

# 예외 단어 30개
fword = [newcount[i][0] for i in range(len(newcount))][:30]
fnumber = [newcount[i][1] for i in range(len(newcount))][:30]
fxs = [i for i, _ in enumerate(fword)]
plt.bar(fxs, fnumber)
plt.ylabel("단어 수")
plt.title("단어 계산 (예외)")
plt.xticks([i + 0.5 for i, _ in enumerate(fword)], fword, rotation = 90)
plt.show()

print("""예외 되지 않은 단어 30개:""", counts_to_frame[:30])
# 예외 되지 않은 단어 30개
word = [counts[i][0] for i in range(len(counts))][:30]
number = [counts[i][1] for i in range(len(counts))][:30]
xs = [i for i, _ in enumerate(word)]
plt.bar(xs, number)
plt.ylabel("단어 수")
plt.title("단어 계산 (예외 안됨)")
plt.xticks([i + 0.5 for i, _ in enumerate(fword)], fword, rotation = 90)
plt.show()

#숫자 계산
numcount = []
for i in range(len(counts)):
    try :
        numcount.append((int(counts[i][0]), counts[i][1]))
    except ValueError:
        pass

numcount_to_frame = pd.DataFrame(numcount[:30], columns=["Number", "Counts"])
numsum = sum(numcount_to_frame["Counts"])
per3 = [(numcount_to_frame["Counts"][i]/numsum) * 100 \
        for i in range(len(numcount_to_frame))]
numcount_to_frame["Per"] = np.array(per3)
print("""단어 30개:""", numcount_to_frame)

numcount = numcount[:30]
num = [numcount[i][0] for i in range(len(numcount))][:30]
xs = [i for i, _ in enumerate (numcount)]

plt.bar(xs, numcount_to_frame["Counts"])
plt.ylabel("Counts")
plt.xticks([i + 0.5 for i, _ in enumerate (num)], num, rotation = 90)
plt.title("단어 계산")
plt.show()

