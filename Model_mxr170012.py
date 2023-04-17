# Motalib Rahim
# mxr170012
# Dr. Karen Mazidi

# nltk.download('punkt')
# nltk.download('wordnet')
import random  # chooses diff replies
import json
import pickle  # serilization
import numpy as np
import nltk
from tensorflow.keras.models import Sequential  # model
from tensorflow.keras.layers import Dense, Activation, Dropout  # layers
from tensorflow.keras.optimizers import SGD  # gradient
from nltk.stem import WordNetLemmatizer  # reduce to stem

lemma = WordNetLemmatizer()  # lemmatize

targets = json.loads(open('targets.json').read())  # load file

# lists
texts = []  # no of texts
types = []  # no of types
docs = []  # no of doc
stop_words = [',', '.', '!', '?']  # ignores

# iterate over targets
for target in targets['targets']:
    for system in target['system']:
        text_lst = nltk.word_tokenize(system)  # list of text
        texts.extend(text_lst)  # add to list
        docs.append((text_lst, target['tag']))  # list belong to tag
        if target['tag'] not in types:  # if does not exist in types
            types.append(target['tag'])

texts = [lemma.lemmatize(text) for text in texts if text not in stop_words]  # lemmatize
texts = sorted(set(texts))  # for duplicates
types = sorted(set(types))

pickle.dump(texts, open('texts.pickle', 'wb'))  # store in file
pickle.dump(types, open('types.pickle', 'wb'))  # store in file

# numeric value
train = []
output = [0] * len(types)  # 0 as many types

# doc will be in 'train' to train nn
for doc in docs:
    b = []  # empty bag
    text_sys = doc[0]  # system in doc
    text_sys = [lemma.lemmatize(text.lower()) for text in text_sys]
    for text in texts:  # if occurs in sys
        b.append(1) if text in text_sys else b.append(0)

    out = list(output)  # takes in list
    out[types.index(doc[1])] = 1
    train.append([b, out])  # append to train

random.shuffle(train)  # randomize
train = np.array(train)  # arrray

# values, labels to feed nn
x_train = list(train[:, 0])
Y_train = list(train[:, 1])

m = Sequential()  # model
m.add(Dense(128, input_shape=(len(x_train[0]),), activation='relu'))  # layers
m.add(Dropout(0.5))  # prevent overfit
m.add(Dense(64, activation='relu'))  # layer
m.add(Dropout(0.5))
m.add(Dense(len(Y_train[0]), activation='softmax'))  # layer to check no of neurons

gradient = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
# compile model
m.compile(loss='categorical_crossentropy', optimizer=gradient, metrics=['accuracy'])
# fit model, data is fed 200x
g = m.fit(np.array(x_train), np.array(Y_train), epochs=200, batch_size=5, verbose=1)
# save model
m.save('jarvis.h5', g)
print("end")
