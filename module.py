import os
import json
import datetime
from pymongo import MongoClient
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt
import urllib
import pandas as pd

# return list 안에 dict
def execute(key):
    os.system("scrapy crawl cr -o a.json -a keyword="+str(key))
    with open('a.json',encoding='utf-8') as json_file:
        data = json.load(json_file)
    os.remove('./a.json')
    
    return data


# keyword, text 둘다 string
def related_keyword_w2v(keyword, text):
    # 10번 돌리기
    list1 = []
    data_list = []
    list1.append(text)
    data_list.append(list1)
    
    for news_per_keyword in data_list:
        # 데이터 전처리
        # urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings.txt", filename="ratings.txt")
        # train_data = pd.read_table('ratings.txt')
        train_data = news_per_keyword
        # train_data = train_data.dropna(how='any')  # Null 값이 존재하는 행 제거
        # print(train_data.isnull().values.any())  # Null 값이 존재하는지 확인
        # train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
        train_data = [w.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "") for w in train_data]
        stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
        print(train_data)  # 리스트들 출력

        okt = Okt()
        tokenized_data = []
        for sentence in train_data:
            temp_X = okt.morphs(sentence, stem=True)  # 토큰화
            temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
            tokenized_data.append(temp_X)

        # w2v 돌리기
        model = Word2Vec(sentences=tokenized_data, vector_size=100, window=5, min_count=5, workers=4, sg=0)
        # model.wv.vectors.shape  # shape 보기

        # 테스팅
        return model.wv.most_similar(keyword)

