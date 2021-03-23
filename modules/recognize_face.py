from neural_networks.recognitionFace import FaceRecognition
from .base import Module

class RecognizeFace(Module):
    def exec(self):
        recognition_face = FaceRecognition("PEOPLES")
        recognition_face.load(f"models/{str(recognition_face)}")
        ans = recognition_face.predict("logs/images/image_0.jpg")
        if ans != None:
            self.people_name, self.people_hobby = ans
        return ''