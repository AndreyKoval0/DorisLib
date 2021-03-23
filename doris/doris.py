from neural_networks.textClassification import Classifier
import pymorphy2


class Doris:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.models = [Classifier("He"),
                Classifier("Me"),
                Classifier("FAQ"),
                Classifier("ORDER"),
                Classifier("Statement")]
    def train(self, epochs=500):
        for i in range(len(self.models)):
            print(self.models[i])
            self.models[i].train(epochs)

    def Append(self, l):
        lens = list(map(len, l))
        for i in range(len(l)):
            while len(l[i]) < max(lens):
                l[i].append(None)
        return l

    def Index(self, l, n, m=-1):
        ans = []
        if n >= len(l[0]):
            return ans
        for i in range(len(l)):
            if m == -1: ans.append(l[i][n])
            else: ans.append(l[i][n:m])
        return ans

    def GetAction(self, question):
        pred = question.replace(',', '').replace('?', '').replace('!', '').replace('.', '').split(' ')
        action = None
        tags = []

        for j in range(len(pred)):
            tags.append(str(self.morph.parse(pred[j])[0].tag).split(','))
        tags = self.Append(tags)
        
        if len(tags) != 0:
            if 'NPRO' in self.Index(tags, 0) and '2per sing' in self.Index(tags, 1):
                action = 0
            elif ['NPRO', '1per sing', 'nomn'] in self.Index(tags, 0,3):
                action = 1
            elif 'NPRO' in self.Index(tags, 0) and '1per plur' in self.Index(tags, 1):
                action = 0
            elif 'VERB' in self.Index(tags, 0) and '2per' in self.Index(tags, 3):
                action = 0
            elif 'INFN' in self.Index(tags, 0):
                action = 0
            elif 'Ques' in self.Index(tags, 1) or 'CONJ' in self.Index(tags, 0) or ['NPRO', 'masc sing', 'nomn'] in self.Index(tags, 0,3):
                action = 2
            elif ['VERB','perf','tran sing'] in self.Index(tags, 0,3):
                action = 3
            else:
                action = 4
        return action
    
    def predict(self, question):
        action = self.GetAction(question)
        ans = self.models[action].predict(question)
        return ans
    
    def save(self):
        for i in range(len(self.models)):
            self.models[i].save("models/" + str(self.models[i]))
    def load(self):
        for i in range(len(self.models)):
            self.models[i].load("models/" + str(self.models[i]))        


def train(doris):
    doris.train(700)
    doris.save()

def add_training(doris):
    doris.load()
    doris.train(400)
    doris.save()