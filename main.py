import fasttext
from fb_scraper import FBCollector
import os.path

collect_data = False    # True if new data from FogBugz should be collected. Existing data will be used otherwise
training = True     # True if a new model should be trained. An existing model will be used otherwise

if collect_data or not os.path.isfile('train.txt') or not os.path.isfile('test.txt'):
    collector = FBCollector()
    print('Hold on, collecting FogBugz case data...')
    collector.collect('train.txt', (800000, 830000))
    collector.collect('test.txt', (830000, 831000))

if training or not os.path.isfile('model.bin'):
    print('Training classifier...')
    classifier = fasttext.supervised('train.txt', 'model')
    print('Done!')
else:
    classifier = fasttext.load_model('model.bin')

testing = classifier.test('test.txt', 1)

results = '''Test samples: {}
Precision: {}
Recall: {}'''
print(results.format(testing.nexamples, testing.precision, testing.recall))
