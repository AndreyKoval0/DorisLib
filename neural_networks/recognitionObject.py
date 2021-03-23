import os
import cv2
import keras
import numpy as np
from keras.utils import np_utils
from neural_networks.base import Base

class ObjectRecognition(Base):
    def __init__(self):
        self.nameClass = []
        self.loadData()
    
    def loadImg(self, name_img):
        img = cv2.imread(name_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (56, 56))
        return img

    def loadData(self):
        path = os.listdir("images/")
        filepath = []
        for i in path:
            pathDir = os.listdir("images/" + i)
            if not ("." in i):
                self.nameClass.append(i)
            for j in pathDir:
                if ".jpg" in j.lower():
                    filepath.append(f"images/{i}/{j}")
        train_data = []
        for file in filepath:
            train_data.append(self.loadImg(file))

        self.y_train = []
        for i in filepath:
            self.y_train.append(self.nameClass.index(i.split("/")[1]))

        self.X_train = np.array(train_data)
        self.y_train = np_utils.to_categorical(np.array(self.y_train))

    def buildModel(self):
        base_model = keras.applications.vgg16.VGG16(include_top=False, weights="imagenet", input_shape=(56, 56, 3),
                                                    pooling='avg')
        base_model.layers.pop()
        for layer in base_model.layers:
            layer.trainable = False

        x = base_model.output
        x = keras.layers.Dense(512, activation="relu")(x)
        x = keras.layers.Dense(len(self.y_train[0]), activation="softmax")(x)
        model = keras.models.Model(inputs=[base_model.input], outputs=[x])

        model.compile(loss='categorical_crossentropy',
                    optimizer="rmsprop",
                    metrics=['accuracy']) 
        return model
    
    def train(self, epochs=10):
        self.model = self.buildModel()
        datagen = keras.preprocessing.image.ImageDataGenerator(
            featurewise_center=True,
            featurewise_std_normalization=True,
            rotation_range=20,
            width_shift_range=0.001,
            height_shift_range=0.001,
            horizontal_flip=True)

        datagen.fit(self.X_train)
        self.model.fit_generator(datagen.flow(self.X_train, self.y_train, batch_size=32),
                            steps_per_epoch=len(self.X_train) / 32,
                            epochs=epochs)
    
    def predict(self, x_pred):
        name_img = x_pred
        img = np.array([self.loadImg(name_img)])
        return self.nameClass[np.argmax(self.model.predict(img))]
    
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
        return "ObjectRecognition()"