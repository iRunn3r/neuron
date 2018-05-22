from fogbugz_tools import FB
from fasttext_tools import FT
import os
import data
import pickle
import time
import datetime
import HTML

MODEL_NAME = 'model.bin'
TRAINING_FILE = 'training.text'
TESTING_FILE = 'testing.text'
COLLECT_TRAINING = False
COLLECT_TESTING = True
TRAIN_MODEL = False
fb = FB()
ft = FT()

bug_query = 'case:{}...{} AND rating:"0...5" AND (category:"bug" AND (status:"Fixed" OR status:"Duplicate" OR status:"postponed"))'
incident_query = 'case:{}...{} AND rating:"0...5" AND (category:"QA Incoming Incident" AND (-status:"duplicate" AND status:"closed"))'
day_0_query = 'assignedTo:"qa Incoming" AND status:"active (new)" and (Version:\'5.6.*\' or Version:\'2017.*\' ' \
              'or Version:\'2018.*\' and opened:”6/26/2017..”)'

LOW_BOUND = 800000
HIGH_BOUND = 1050000
SEARCH_STEP = 1000

if COLLECT_TRAINING:
    training_cases = []
    iteration_durations = []
    remaining_time = 'N/A'
    for i in range(LOW_BOUND, HIGH_BOUND, SEARCH_STEP):
        start_time = int(time.time())
        found_bugs = fb.search(bug_query.format(i, i + SEARCH_STEP), max_results=SEARCH_STEP)
        found_incidents = fb.search(incident_query.format(i, i + SEARCH_STEP), max_results=len(found_bugs))
        print('Found bugs/incidents: {}/{}. Search bounds: {}-{}. Estimated time remaining: {}.'.format(len(found_bugs), len(found_incidents), i, i + SEARCH_STEP, remaining_time), end='\r')
        total_found = found_bugs + found_incidents
        training_cases += total_found
        with open(os.path.join(data.PROJECT_ROOT, 'temp.pkl'), 'w+b') as f:
            pickle.dump(training_cases, f)
        end_time = int(time.time())
        iteration_durations.append(end_time-start_time)
        remaining_time = str(datetime.timedelta(seconds=(sum(iteration_durations) / len(iteration_durations))))
    training_file = ft.preprocess(training_cases, outfile=TRAINING_FILE)
    model = ft.train(training_file)
else:
    model_path = os.path.join(data.PROJECT_ROOT, MODEL_NAME)
    if os.path.isfile(model_path) and not TRAIN_MODEL:
        model = ft.load(model_path)
    else:
        training_data = os.path.join(data.PROJECT_ROOT, TRAINING_FILE)
        if os.path.isfile(training_data):
            model = ft.train(training_data, MODEL_NAME)
        else:
            raise Exception('Model could not be loaded - no training data found.')


day_0_cases = fb.search(day_0_query)
predictions = []
for case in day_0_cases:
    prediction = model.predict(' '.join([case.title, case.body]))
    if prediction[0][0] == '__label__incident':
        probability = 1.0 - prediction[1][0]
    else:
        probability = prediction[1][0]
    predictions.append([case.number, abs(int(probability * 100)), case.title])
print(datetime.datetime.now())
predictions.sort(key=lambda x: x[1], reverse=True)
HTML.create_table(predictions)
