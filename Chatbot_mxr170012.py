# Motalib Rahim
# mxr170012
# Dr. Karen Mazidi

import nltk
from nltk.stem import WordNetLemmatizer # reduce to stem
import numpy as np
import pickle # serialization
import json
import random # chooses replies
import tensorflow as tf
from tensorflow.keras.models import load_model

lemma = WordNetLemmatizer() # lemmatize
targets = json.loads(open('targets.json').read()) # load file

texts = pickle.load(open('texts.pickle', 'rb')) # load text
types = pickle.load(open('types.pickle', 'rb')) # load types
m = load_model('jarvis.h5')

# for specific user a usermodel
class user_model:
    def __init__(self, name=None, personal_info=None, likes=None, dislikes=None):
        self.name = name
        self.personal_info = personal_info
        self.likes = likes
        self.dislikes = dislikes

# clean sentence
def clean_sent(sent):
  sent_txt = nltk.word_tokenize(sent) # tokenize
  sent_txt = [lemma.lemmatize(text) for text in sent_txt] # lemmatize
  return sent_txt

# get bow, if text exist
def bow(sent):
  sent_txt = clean_sent(sent)
  b = [0] * len(texts)
  for t in sent_txt: # set values
    for i, text in enumerate(texts):
      if text == t:
        b[i] = 1
  return np.array(b)

# predict types based on sent
def find_types(sent):
  bows = bow(sent) # bow created to be fed into nn
  comp = m.predict(np.array([bows]))[0] # prediction
  error = 0.20 # error allowance
  f_comps = [[i, c] for i, c in enumerate(comp) if c > error] # enumerate to get index, prob

# sort
  f_comps.sort(key =lambda z: z[1], reverse=True) # to get top probability
  re_lst = []
  for c in f_comps:
    re_lst.append({'target': types[c[0]], 'probability': str(c[1])}) # list targets and prob
  return re_lst

# generate response
def reply(target_lst, target_json, name):
  tag = target_lst[0]['target']
  lst_targets = target_json['targets']
  for t in lst_targets:
    if t['tag'] == tag:
       out_c = random.choice(t['replies'])
       break
  return out_c

user = user_model()

print("This is Jarvis, ask away!")

while True:
  text_msg = input("")
  if user not in user.__dict__:
    user.name = text_msg
  find = find_types(text_msg)
  re = reply(find, targets, user)
  print(re)