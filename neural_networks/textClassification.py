import tensorflow.keras as keras
#import keras
import numpy as np
import pymorphy2
import pandas as pd
import sqlite3
from keras.utils import np_utils
from neural_networks.base import Base

morph = pymorphy2.MorphAnalyzer()


class Classifier(Base):
    def __init__(self, table_name):
        super().__init__(table_name)
        self.loadData()
        self.getAllWord()
        self.prepareData()

    def bagWord(self, words):
        vec = [0] * len(self.all_words)
        for word in words:
            if word in self.all_words:
                vec[self.all_words.index(word)] += 1
        return vec

    def buildModel(self):
        model = keras.Sequential([
            keras.layers.Dense(units=10, input_shape=[len(self.X_train[0])], activation="relu"),
            keras.layers.Dense(units=10, activation="relu"),
            keras.layers.Dense(units=len(self.y_train[0]), activation="softmax")
        ])
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def getAllWord(self):
        self.all_words = []
        self.prepared_questions = []
        for i in range(len(self.data["Question"])):
            tmp = []
            row = [self.data["Question"][i].strip().split(),
                   self.data["Answer"][i].strip().split()] 
            for word in row[0]:
                prepared_word = morph.parse(word.lower().replace("?", "").replace("!", "").replace(".", ""))[0].normal_form
                tmp.append(prepared_word)
                self.all_words.append(prepared_word)
            for word in row[1]:
                prepared_word = morph.parse(word.lower().replace("?", "").replace("!", "").replace(".", ""))[0].normal_form
                self.all_words.append(prepared_word)
            self.prepared_questions.append(tmp)
        self.all_words = list(sorted(set(self.all_words)))

    def loadData(self):
        conn = sqlite3.connect('memory.db')

        query = f"SELECT * FROM '{self.table_name}'"

        self.data = pd.read_sql_query(query, conn)
    
    def prepareX(self):
        self.X_train = []
        for words in self.prepared_questions:
            self.X_train.append(self.bagWord(words))
        self.X_train = np.array(self.X_train)
    
    def prepareY(self):
        self.y_train = []
        all_answers = list(sorted(set(self.data["Answer"])))
        for answer in self.data["Answer"]:
            self.y_train.append(all_answers.index(answer))
        self.y_train = np_utils.to_categorical(np.array(self.y_train), max(self.y_train) + 1)

    def prepareData(self):
        self.prepareX()
        self.prepareY()
    
    def train(self, epochs):
        self.model = self.buildModel()
        self.model.fit(self.X_train,
                       self.y_train,
                       epochs=epochs,
                       verbose=2)
    
    def predict(self, x_pred):
        question = list(map(lambda x: morph.parse(x.lower().replace("?", "").replace("!", "").replace(".", ""))[0].normal_form,
                            x_pred.strip().split()))
        X_pred = np.array([self.bagWord(question)])
        y_pred = np.argmax(self.model.predict(X_pred))
        Y_train = list(self.y_train)
        for i in range(len(Y_train)):
            Y_train[i] = np.argmax(self.y_train[i])
        return self.data["Answer"][list(Y_train).index(y_pred)]

    def save(self, fname):
        json_file = f'{fname}.json'
        model_json = self.model.to_json()

        with open(json_file, 'w+') as f:
            f.write(model_json)

        self.model.save_weights(f'{fname}.h5')
    
    def load(self, fname):
        json_file = f'{fname}.json'

        with open(json_file, 'r') as f:
            self.model = keras.models.model_from_json(f.read())
        
        self.model.load_weights(f'{fname}.h5')
    
    def __str__(self):
        return f"Classifier({self.table_name})"
