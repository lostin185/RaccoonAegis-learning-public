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

from konlpy.tag import Okt
okt = Okt()

morpheme = []

for text in texts:
  union = ""
  for word_tag in okt.pos(text, norm=True, stem=True):
    if word_tag[1] in ['Noun', 'Verb', 'VerbPrefix', 'Adjective', 'Determiner', 'Adverb', 'Exclamation', 'KoreanParticle']:
      union += word_tag[0]
      union += " "
  morpheme.append(union)  

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np

maxlen = 50
max_words = 10000

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(morpheme)
sequences = tokenizer.texts_to_sequences(morpheme)
word_index = tokenizer.word_index
print('%s개의 고유한 토큰을 찾았습니다.' % len(word_index))

# word_index 저장
import json
json = json.dumps(word_index)
f3 = open("wordIndex.json", "w")
f3.write(json)
f3.close()

data = pad_sequences(sequences, maxlen=maxlen)
labels = np.asarray(labels)
print('데이터 텐서의 크기:', data.shape)
print('레이블 텐서의 크기:', labels.shape)

indices = np.arange(data.shape[0])
np.random.shuffle(indices)
x_train = data[indices]
y_train = labels[indices]

# 순환 컨볼루션 신경망 모델
from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop
from keras import regularizers

model = Sequential()
model.add(layers.Embedding(max_words, 32, input_length=maxlen))
model.add(layers.Dropout(0.5))
model.add(layers.Conv1D(64, 3, padding='valid', activation='relu', strides=1))
model.add(layers.MaxPooling1D(pool_size=4))
model.add(layers.LSTM(32))
model.add(layers.Dense(16, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(16, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.summary()

model.compile(optimizer='adam',
  loss='binary_crossentropy',
  metrics=['acc'])

history = model.fit(x_train, y_train,
  epochs=10,
  batch_size=64,
  validation_split=0.2)

from keras.models import load_model
model.save('model.h5')

import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
