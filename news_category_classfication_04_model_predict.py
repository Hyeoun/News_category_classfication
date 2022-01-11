import pandas as pd
import numpy as np
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import *
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)

df = pd.read_csv('./crawling/naver_headline_news20211116.csv')
print(df.head())
print(df.info())

X = df['title']
Y = df['category']

# ============= Y에 대한 onehotencoding 로드===========================
with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
labeled_Y = encoder.transform(Y)
label = encoder.classes_
print(labeled_Y[0])
onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)
# ===============================================================

okt = Okt()

for i in range(len(X)):
    X[i] = okt.morphs(X[i])

stopwords = pd.read_csv('./crawling/stopwords.csv', index_col=0)
print(stopwords.head())

# 의미 없는 단어 제거
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1 and X[j][i] not in list(stopwords['stopword']):
            words.append(X[j][i])
    X[j] = ' '.join(words)
print(X)

# 단어를 숫자에 대응
with open('./models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])
Max = 23
for i in range(len(tokened_X)):
    if Max < len(tokened_X[i]):
        tokened_X[i] = tokened_X[i][:Max]  # 혹시 Max값보다 크면 Max값에 맞춘다.

X_pad = pad_sequences(tokened_X, Max)
print(X_pad[:10])

# model.Load
# model.predict(tokened_X)
# predict과 onehot_Y와 비교

model = load_model('./models/news_category_classfication_model_0.7328135967254639.h5')

# while True:
#     my_sample = np.random.randint(200)
#     sample = X_pad[my_sample]
#     sample = sample.reshape(-1, Max)
#     news_category_predict = model.predict(sample)
#     print('========================================================================')
#     print(label)
#     print(X[my_sample])
#     print('actual is : ', onehot_Y[my_sample])
#     print('Pred is : ', news_category_predict[0])
#     print('Target : ', label[np.argmax(onehot_Y[my_sample])])
#     print('Prediction after learning is : ', label[np.argmax(news_category_predict)])
#     if input('종료하시겠습니까? 종료:1 / 계속:아무키 ') == '1': break

preds = model.predict(X_pad)
predicts = []
for pred in preds:
    predicts.append(label[np.argmax(pred)])
print(predicts)
df['predict'] = predicts
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 20)  # 최대 열수 지정

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] == df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 'O'
    else: df.loc[i, 'OX'] = 'X'
print(df.head(10))
print(df['OX'].value_counts()/len(df))