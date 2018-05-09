from fogbugz import FogBugz, FogBugzConnectionError, FogBugzAPIVersionError, FogBugzLogonError, FogBugzAPIError
import re
import os
from case import Case
import math


class FB:
    def __init__(self):
        token = os.environ.get('FOGBUGZ_TOKEN')
        self.criteria = 'ixBug,sStatus,sOriginalTitle,sCategory,events'
        if token:
            try:
                self.__fogbugz = FogBugz('https://fogbugz.unity3d.com', token=token, api_version=8)
                self.__fogbugz.search(q='1000000')
            except (FogBugzConnectionError, FogBugzAPIVersionError, FogBugzLogonError, FogBugzAPIError) as e:
                raise e
        else:
            raise Exception('FogBugz API key "FOGBUGZ_TOKEN" is not set up in your environment variables.')

    @staticmethod
    def get_status(status):
        if status == "Bug":
            return "bug"
        elif status == "QA Incoming Incident":
            return "incident"
        else:
            return "?"

    def collect_info(self, case):
        title = re.sub('\W+', ' ', case.sOriginalTitle.text.lower())
        if case.events.event.s:
            body = re.sub('\W+', ' ', case.events.event.s.text.lower())
            body = re.sub('1 what happened', '', body)
            body = re.sub('2 how .+ reproduce it using the example you attached', '', body)
        else:
            body = ''
        number = case.ixBug.text
        status = self.get_status(case.sCategory.text)
        return Case(number, status, title, body)

    def search(self, query, columns=None):
        result = []
        resp = self.__fogbugz.search(q=query, cols=columns if columns else self.criteria, max=5000)
        for case in resp.cases.childGenerator():
            entry = self.collect_info(case)
            result.append(entry)
        return result

    def search_range(self, query, bounds, columns=None, step=5000):
        result = []
        bottom_bound = bounds[0]
        iterations = int(math.ceil((bounds[1] - bounds[0]) / float(step)))
        for i in range(iterations):
            if bottom_bound + step >= bounds[1]:
                top_bound = bounds[1]
            else:
                top_bound = bottom_bound + step
            print('Currently processing: {} - {}'.format(bottom_bound, top_bound))
            resp = self.__fogbugz.search(q='case:"{}...{}" AND '.format(bottom_bound, top_bound) + query,
                                         cols=columns if columns else self.criteria, max=step)
            found_cases = resp.cases.childGenerator()
            for case in found_cases:
                entry = self.collect_info(case)
                result.append(entry)
            print('Total cases found: {}'.format(len(result)))
            bottom_bound = top_bound
        return result
