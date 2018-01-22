import re
import string


class Cleaner:
    def __init__(self):
        self.__printable = set(string.printable)
    
    def __remove_tags(self, text):
        pattern = re.compile('<.*?>')
        return re.sub(pattern, '', str(text))

    def __remove_junk(self, text, title):
        junk = ['License type: Pro', 'License type: Free', '1.* What happened',
                '2.* How .* reproduce it using the example you attached', 'Public status: Public',
                '\n', '\t', '\r', '\s+']
        text = text.replace(title, '')
        for pattern in junk:
            text = re.sub(re.compile(pattern), ' ', text)
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

        return {'number': number, 'status': status, 'title': title, 'body': body}
