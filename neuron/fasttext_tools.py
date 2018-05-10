import fastText
import data
import os


class FT:
    @staticmethod
    def tokenize(case):
        return '__{}__ {} {}\n'.format(case.status, case.title, case.body)

    def preprocess(self, cases, outfile='processed.text'):
        with open(os.path.join(data.PROJECT_ROOT, outfile), 'w+') as f:
            for case in cases:
                f.write(self.tokenize(case))

    @staticmethod
    def train(training_data, outfile='model.bin'):
        model_path = os.path.join(data.PROJECT_ROOT, outfile)
        model = fastText.train_supervised(input=training_data, epoch=25, lr=1.0, wordNgrams=2, verbose=2, minCount=1)
        model.save_model(model_path)
        return model_path

    @staticmethod
    def test(model, test_data):
        test_results = model.test(test_data)
        return {'sample_count': test_results[0], 'precision': test_results[1], 'recall': test_results[2]}

    @staticmethod
    def predict(model, text: str):
        prediction = model.predict(text)
        return prediction
