import fasttext
from fb_scraper import FBCollector

collector = FBCollector()
# query = '''assignedTo:"QA Incoming" AND status:"Active (New)" AND (Version:'5.6.*' OR Version:'2017.*' OR Version:'2018.*' AND opened:”6/26/2017..”)'''
query = '''assignedTo:"QA Incoming" AND status:"Active (New)" AND (iossupport OR iOS OR xcode OR tvOS OR AppleTVSupport AND Version:'5.6.*' or Version:'2017.*' or Version:'2018.*' AND opened:”6/26/2017..” OR supportxcustomer:"Premium" OR supportxcustomer:"Enterprise" AND assignedto:"QA Incoming" OR assignedto:"QA Student worker grabbag")'''

cases = collector.simple_search(query)
classifier = fasttext.load_model('model.bin')

with open('predictions.txt', 'w') as out_file:
    for case in cases:
        prediction = classifier.predict_proba(['.'.join([case['title'], case['body']])])
        if prediction[0][0][0] == '__label__bug':
            case.update({"probability": prediction[0][0][1]})
        else:
            case.update({"probability": 1 - prediction[0][0][1]})
        out_file.write(' '.join([case['number'], str(case['probability']) + '\n']))
