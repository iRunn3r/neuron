import fastText
import data
import os


class Model:
    def __init__(self, path):
        self.model = fastText.load_model(path)

    def predict(self, text: str):
        prediction = self.model.predict(text)
        return prediction

    def test(self, test_data):
        results = self.model.test(test_data)
        return results


class FT:
    @staticmethod
    def tokenize(case):
        return '__label__{} {} {}\n'.format(case.status, case.title, case.body)

    def preprocess(self, cases, outfile):
        with open(os.path.join(data.PROJECT_ROOT, outfile), 'w+') as f:
            for case in cases:
                f.write(self.tokenize(case))
        return os.path.join(data.PROJECT_ROOT, outfile)

    @staticmethod
    def train(training_data, outfile='model.bin'):
        model_path = os.path.join(data.PROJECT_ROOT, outfile)
        model = fastText.train_supervised(input=training_data, epoch=35, lr=1.0, wordNgrams=5, verbose=2, minCount=1)
        model.save_model(model_path)
        return Model(model_path)

    @staticmethod
    def load(path):
        return fastText.load_model(path)
