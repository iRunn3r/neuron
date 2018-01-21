from fogbugz import FogBugz
import cleaner
import json

with open('keys.json', 'r') as f:
    login_data = json.load(f)

fb = FogBugz(login_data['address'], login_data['token'], api_version=9)
print(fb)
cl = cleaner.Cleaner()

query_step = 1000
search_bounds = (800000, 810000)

criteria = 'ixBug,sStatus,sOriginalTitle,sCategory,events'


for lower_bound in range(search_bounds[0], search_bounds[1], 1000):
    upper_bound = lower_bound + query_step
    bug_query = '(case:"{}...{}" AND rating:"0...5" AND category:"bug" AND (status:"Fixed" OR status:"Duplicate" OR status:"postponed"))'.format(lower_bound, upper_bound)
    incident_query = '(case:"{}...{}" AND rating:"0...5" AND category:"qa Incoming Incident" AND -status:"duplicate" AND status:"closed" )'.format(lower_bound, upper_bound)
    final_query = bug_query + " OR " + incident_query
    resp = fb.search(q=final_query, cols=criteria)
    # for case in resp.cases.childGenerator():
    #     entry = cl.