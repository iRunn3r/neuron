import re
import string


class Cleaner:
    def __init__(self):
        self.__printable = set(string.printable)

    def __remove_tags(self, text):
        pattern = re.compile('<.*?>')
        return re.sub(pattern, '', str(text))

    def __remove_junk(self, text, title):
        text = text.replace(title, '')
        text = text.replace('License type: Pro', '')
        text = text.replace('License type: Free', '')
        text = text.replace('1. What happened', '')
        text = text.replace('2. How we can reproduce it using the example you attached', '')
        text = re.sub(' +', ' ', text.replace('\n', ' '))
        return text

    def __get_status(self, status):
        if status == "Bug":
            return "bug"
        elif status == "QA Incoming Incident":
            return "incident"
        else:
            return "?"

    def clean(self, case):
        title = self.__remove_tags(case.sOriginalTitle)

        body = self.__remove_tags(case.events.event.s)
        body = self.__remove_junk(body, title)
        filter(lambda x: x in self.__printable, body)

        number = self.__remove_tags(case.ixBug)

        status = self.__remove_tags(case.sCategory)
        status = self.__get_status(status)

        return {'number': number, 'title': title, 'body': body, 'status': status}