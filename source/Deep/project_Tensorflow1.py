from collections import Counter
import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def count_whole(dataM):
    f = open(dataM, 'r')
    data = f.read()

    parse = re.sub("[^0-9a-zA-Z\\s]", "", data)
    parse = parse.lower().split()

    counts = Counter(parse)
    counts = counts.most_common()
    counts_to_frame = pd.DataFrame(counts, columns = ["Word", "Counts"])
    countsum1 = sum(counts_to_frame["Counts"])
    per1 = [(counts_to_frame["Counts"][i] / countsum1) * 100 \
            for i in range(len(counts_to_frame))]
    counts_to_frame["Per"] = np.array(per1)

    print("""예외된 단어 30개:""", counts_to_frame[:30])

    word = [counts[i][0] for i in range(len(counts))][:30]
    number = [counts_to_frame[i][1] for i in range(len(counts))][:30]
    xs = [i for i, _ in enumerate(word)]
    plt.bar(xs, number)
    plt.ylabel("Counts")
    plt.title("예외 안된 단어 데이터")
    plt.xticks([i + 0.5 for i,  _ in enumerate(word)], word, rotation = 90)
    plt.show()

def count_filtered(dataM):
        f = open(dataM, 'r')
        data = f.read()

        parse = re.sub("[^0-9a-zA-Z\\s]", "", data)

        parse = parse.lower().split()

        counts = Counter(parse)
        counts = counts.most_common()
        counts_to_frame = pd.DataFrame(counts, columns=["Word", "Counts"])
        countsum1 = sum(counts_to_frame["Counts"])

        articles = ["a", "the" "an"]
        conjunctions = ["and", "but", "or", "as", "if", "when", "than", "because", "while", "where", "after", "so", "thought", "since", "until", "whether", "before", "althought", "nor", "like", "once", " unless", "now", "except"]
        pronouns = ["i", "we", "me", "us", "you", "she" ,"he", "her", "him", "it", "they", "them", "this", "these", "that", "those", "all", "any", "most", "none", "some", "what", "who", "which", "whom", "whose", "my", "your", "its", "our", "their", "something", "nothing", "anything", "himself", "everything", "someone", "themselves", "itself", "anyone" ,"myself"]
        # 한글 형태소로 변환하면 많은 형태소가 나오니껜 확인하고 인코딩 부탁

        blacklist = articles + conjunctions + pronouns

        length = len(counts)
        newcount = []
        for i in range(length):
            if counts[i][0] not in blacklist:
                newcount.append(counts[i])

        new_to_frame = pd.DataFrame(newcount, columns = ["Word", "Counts"])
        countsum2 = sum(new_to_frame["Counts"])
        per2 = [(new_to_frame["Counts"][i]/countsum2) * 100 \
                for i in range(len(new_to_frame))]
        new_to_frame["Per"] = np.array(per2)
        print("""예외된 단어 30개:""", new_to_frame[:30])

        fword = [newcount[i][0] for i in range(len(newcount))][:30]
        fnumber = [newcount[i][1] for i in range(len(newcount))][:30]
        fxs = [i for i, _ in enumerate(fword)]
        plt.bar(fxs, fnumber)
        plt.ylabel("Counts")
        plt.title("예외된 단어 데이터")
        plt.xticks([i + 0.5 for i, _ in enumerate(fword)], fword, rotation=90)
        plt.show()

def count_number(dataM):
    f = open(dataM, 'r')
    data = f.read()

    parse = re.sub("[^0-9a-zA-Z\\s]", "", data)

    parse = parse.lower().split()

    counts = Counter(parse)
    counts = counts.most_common()

    numcount = []
    for i in range(len(counts)):
        try :
            numcount.append((int(counts[i][0]), counts[i][1]))
        except ValueError:
            pass

    numcount_to_frame = pd.DataFrame(numcount[:30], columns=["Number", "Counts"])
    numsum = sum(numcount_to_frame["Counts"])
    per3 = [(numcount_to_frame["Counts"][i]/numsum)*100\
            for i in range(len(numcount_to_frame))]
    numcount_to_frame["Per"] = np.array(per3)
    print("""단어 30개:""", numcount_to_frame)

    numcount = numcount[:30]
    num = [numcount[i][0] for i in range(len(numcount))][:30]
    xs = [i for i, _ in enumerate (numcount)]

    plt.bar(xs, numcount_to_frame["Countes"])
    plt.ylabel("Counts")
    plt.xticks([i + 0.5 for i, _ in enumerate (num)], num, rotation = 90)
    plt.title("뭘까????")
    plt.show()