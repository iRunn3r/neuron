import fasttext
from fb_scraper import FBCollector

collect_data = True    # True if new data from FogBugz should be collected. Existing data will be used otherwise
training = True     # True if a new model should be trained. An existing model will be used otherwise

if collect_data:
    collector = FBCollector()
    collector.collect('train.txt', (800000, 830000))
    collector.collect('test.txt', (830000, 831000))

if training:
    classifier = fasttext.supervised('train.txt', 'model')
else:
    classifier = fasttext.load_model('model.bin')

testing = classifier.test('test.txt', 1)
print(testing.nexamples)
