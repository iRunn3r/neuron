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

    def simple_search(self, query):
        result = []
        resp = self.__fb.search(q=query, cols=self.__criteria)
        for case in resp.cases.childGenerator():
            entry = self.__cl.clean(case)
            result.append(entry)
        return result

    def bounded_search(self, queries, search_bounds, query_step, outfile):
        with open(outfile, 'w') as out_file:
            for lower_bound in range(search_bounds[0], search_bounds[1], 1000):
                upper_bound = lower_bound + query_step
                q = []
                for query in queries:
                    q.append(query.format(lower_bound, upper_bound))
                query = ' OR '.join(q)
                response = self.simple_search(query)
                print(len(response))
                for case in response:
                    out_file.write(' '.join(('__label__' + case['status'], case['title'] + '.', case['body'], '\n')))