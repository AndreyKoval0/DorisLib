import os
import cv2
import numpy as np
import pandas as pd
import sqlite3
from neural_networks.base import Base

class FaceRecognition(Base):
    def __init__(self, table_name):
        super().__init__(table_name)
        self.loadData()
    
    def loadData(self):
        conn = sqlite3.connect('memory.db')
        query = f"SELECT * FROM '{self.table_name}'"
        self.data = pd.read_sql_query(query, conn)
        paths = list(self.data["PathToFace"])
        self.face = cv2.CascadeClassifier("haarcascades//haarcascade_frontalface_alt2.xml")
        self.X_train = []
        self.y_train = []
        for i in range(len(paths)):
            for root, _, files in os.walk(paths[i]):
                for file in files:
                    path = os.path.join(root, file)
                    img = cv2.imread(path)
                    img = cv2.resize(img, (640, 480))
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
                    faces = self.face.detectMultiScale(img, scaleFactor=1.5, minNeighbors=5)
                    for (x, y, w, h) in faces:
                        roi = img[y:y+h, x:x+w]
                        self.X_train.append(roi)
                        self.y_train.append(i)
    
    def buildModel(self):
        model = cv2.face.LBPHFaceRecognizer_create()
        return model
    
    def train(self):
        self.model = self.buildModel()
        self.model.train(self.X_train, np.array(self.y_train))
    
    def predict(self, x_pred):
        name_img = x_pred 
        img = cv2.imread(name_img)
        img = cv2.resize(img, (640, 480))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face.detectMultiScale(img, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi = img[y:y+h, x:x+w]
            roi = cv2.resize(roi, (550, 550))
            y_pred, conf = self.model.predict(roi)
            if conf >= 45:
                return self.data["Name"][y_pred], self.data["Hobby"][y_pred]
    
    def save(self, fname):
        self.model.save(f"{fname}.yml")
    
    def load(self, fname):
        self.model = self.buildModel()
        self.model.read(f"{fname}.yml")
    
    def __str__(self):
        return f"FaceRecognition({self.table_name})"