import fastText
from fb_scraper import FBCollector
import os.path

collect_data = False    # True if new data from FogBugz should be collected. Existing data will be used otherwise
training = True     # True if a new model should be trained. An existing model will be used otherwise
bug_query = '(case:"{}...{}" AND rating:"0...5" AND category:"bug" AND (status:"Fixed" OR status:"Duplicate" OR status:"postponed"))'
incident_query = '(case:"{}...{}" AND rating:"0...5" AND category:"qa Incoming Incident" AND -status:"duplicate" AND status:"closed" )'

if collect_data or not os.path.isfile('train.txt') or not os.path.isfile('test.txt'):
    collector = FBCollector()
    print('Hold on, collecting FogBugz case data...')
    collector.bounded_search([bug_query, incident_query], (800000, 1033750), 1000, 'train.txt')
    collector.bounded_search([bug_query, incident_query], (980000, 981000), 1000, 'test.txt')

if training or not os.path.isfile('model.bin'):
    print('Training classifier...')
    classifier = fastText.supervised('train.txt', 'model')
    print('Done!')
else:
    classifier = fastText.load_model('model.bin')

testing = classifier.test('test.txt', 1)

results = '''Test samples: {}
Precision: {}
Recall: {}'''
print(results.format(testing.nexamples, testing.precision, testing.recall))
