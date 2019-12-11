# Load Modules
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from konlpy.tag import Okt

# Data
examples = [
  "악플일 확률을 알고싶은 문장을 넣어주세요.",
  "여기에 넣어주시면 됩니다."
  ]

# Tokenize Korean
okt = Okt()
ex_morpheme = []
for text in examples:
  union = ""
  for word_tag in okt.pos(text, norm=True, stem=True):
    if word_tag[1] in ['Noun', 'Verb', 'VerbPrefix', 'Adjective', 'Determiner', 'Adverb', 'Exclamation', 'KoreanParticle']:
      union += word_tag[0]
      union += " "
  ex_morpheme.append(union)

# Data Preprocessing
maxlen = 50
max_words = 10000
tokenizer = Tokenizer(num_words=max_words)
sequences = tokenizer.texts_to_sequences(ex_morpheme)
x_test = pad_sequences(sequences, maxlen=maxlen)

# Load Word Index
import json
with open('wordIndex.json') as json_file:
  word_index = json.load(json_file)
  tokenizer.word_index = word_index

# Load and Use Model
model = load_model('model.h5')
value_predicted = model.predict(x_test)
for i in range(0, len(x_test)):
  print(examples[i], ":", round(value_predicted[i][0] * 100, 1), "%의 확률로 악플입니다.")
  print()