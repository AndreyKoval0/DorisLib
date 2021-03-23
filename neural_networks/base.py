class Base:
    def __init__(self, table_name):
        self.table_name = table_name
    
    def loadData(self):
        pass
    
    def buildModel(self):
        pass

    def train(self, epochs):
        pass

    def predict(self, x_pred):
        pass

    def save(self, fname):
        pass

    def load(self, fname):
        pass

    def __str__(self):
        return f"NeralNetwork({self.table_name})"