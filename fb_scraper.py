from fogbugz import FogBugz
from cleaner import Cleaner
import json


class FBCollector:
    def __init__(self):
        with open('keys.json', 'r') as f:
            self.__login_data = json.load(f)
        self.__fb = FogBugz(self.__login_data['address'], self.__login_data['token'], api_version=9)
        self.__cl = Cleaner()
        self.__criteria = 'ixBug,sStatus,sOriginalTitle,sCategory,events'
        self.__bug_query = '(case:"{}...{}" AND rating:"0...5" AND category:"bug" AND (status:"Fixed" OR status:"Duplicate" OR status:"postponed"))'
        self.__incident_query = '(case:"{}...{}" AND rating:"0...5" AND category:"qa Incoming Incident" AND -status:"duplicate" AND status:"closed" )'

    def collect(self, outfile, search_bounds, query_step=1000):
        with open(outfile, 'w') as out_file:
            for lower_bound in range(search_bounds[0], search_bounds[1], 1000):
                upper_bound = lower_bound + query_step
                final_query = self.__bug_query.format(lower_bound, upper_bound) + " OR " + self.__incident_query.format(lower_bound, upper_bound)
                resp = self.__fb.search(q=final_query, cols=self.__criteria)
                for case in resp.cases.childGenerator():
                    entry = self.__cl.clean(case)
                    out_file.write(' '.join(('__label__' + entry['status'], entry['title'] + '.', entry['body'], '\n')))
