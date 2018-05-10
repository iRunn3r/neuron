from fogbugz_tools import FB
from fasttext_tools import FT

collect_training = False
collect_testing = True
training = True
fb = FB()
ft = FT()

bug_query = '(rating:"0...5" AND (category:"bug" AND (status:"Fixed" OR status:"Duplicate" OR status:"postponed")) ' \
            'OR (category:"QA Incoming Incident" AND (-status:"duplicate" AND status:"closed")))'

cases = fb.search_range(bug_query, (800000, 1034000))
ft.preprocess(cases, outfile='training_800000_1034000.text')
