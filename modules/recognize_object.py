from .base import Module
from neural_networks.recognitionObject import ObjectRecognition

class RecognizeObject(Module):
    def exec(self):
        recognition_object = ObjectRecognition()
        recognition_object.load(f"models/{str(recognition_object)}")
        return recognition_object.predict(f"logs/images/image_0.jpg")