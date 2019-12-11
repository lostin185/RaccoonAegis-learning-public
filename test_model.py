from konlpy.tag import Okt
okt = Okt()

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np

maxlen = 50
max_words = 10000

tokenizer = Tokenizer(num_words=max_words)

import json

with open('wordIndex.json') as json_file:
  word_index = json.load(json_file)
  tokenizer.word_index = word_index

from keras.models import load_model
model = load_model('a_model.h5')

texts = []
labels = []

f1 = open("비속어가 저장된 파일을 지정해주세요", 'r')
f2 = open("비속어 라벨링이 저장된 파일을 지정해주세요", 'r')

while True:
  textline = f1.readline()
  labelline = f2.readline()
  if not textline: break
  texts.append(textline[:-1])
  labels.append(int(labelline[:-1]))

f1.close()
f2.close()

morpheme = []

for text in texts:
  union = ""
  for word_tag in okt.pos(text, norm=True, stem=True):
    if word_tag[1] in ['Noun', 'Verb', 'VerbPrefix', 'Adjective', 'Determiner', 'Adverb', 'Exclamation', 'KoreanParticle']:
      union += word_tag[0]
      union += " "
  morpheme.append(union)  

sequences = tokenizer.texts_to_sequences(morpheme)
data = pad_sequences(sequences, maxlen=maxlen)
labels = np.asarray(labels)

indices = np.arange(data.shape[0])
np.random.shuffle(indices)
x_test = data[indices]
y_test = labels[indices]

value_evaluated = model.evaluate(x_test, y_test)
print("정확도는", round(value_evaluated[1]*100, 2), "%입니다.")