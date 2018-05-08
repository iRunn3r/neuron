import fastText
from fb_scraper import FBCollector

collector = FBCollector()
# query = '''assignedTo:"QA Incoming" AND status:"Active (New)" AND (Version:'5.6.*' OR Version:'2017.*' OR Version:'2018.*' AND opened:”6/26/2017..”)'''
query = '''assignedTo:"QA Incoming" AND status:"Active (New)" AND (androidplayer OR android OR gvr OR gear OR Daydream OR cardboard OR ouya AND Version:'2018.*' or Version:'5.6.*' or Version:'2017.*' AND opened:”6/26/2017..” OR supportxcustomer:"Premium" OR supportxcustomer:"Enterprise" AND assignedto:"QA Incoming" OR assignedto:"QA Student worker grabbag")'''

cases = collector.simple_search(query)
classifier = fastText.load_model('model.bin')

for case in cases:
    prediction = classifier.predict_proba(['.'.join([case['title'], case['body']])])
    if prediction[0][0][0] == '__label__bug':
        case.update({"probability": prediction[0][0][1]})
    else:
        case.update({"probability": 1 - prediction[0][0][1]})
cases.sort(key=lambda x: x['probability'], reverse=True)

with open('predictions.txt', 'w') as out_file:
    for case in cases:
        out_string = ' '.join([case['number'], '{0:.2f}%'])
        out_string = out_string.format(case['probability'] * 100)
        out_file.write(''.join([out_string, '\n']))
