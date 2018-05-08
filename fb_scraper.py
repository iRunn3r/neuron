from fogbugz import FogBugz
import cleaner
import os


class FBCollector:
    def __init__(self):
        self.__fb = FogBugz('https://fogbugz.unity3d.com', os.environ.get('FOGBUGZ_TOKEN'), api_version=8)
        self.__criteria = 'ixBug,sStatus,sOriginalTitle,sCategory,events'

    def simple_search(self, query):
        result = []
        resp = self.__fb.search(q=query, cols=self.__criteria)
        for case in resp.cases.childGenerator():
            entry = cleaner.clean(case)
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
                    out_file.write(' '.join(('__label__' + case.status, case.title + '.', case.body, '\n')))
