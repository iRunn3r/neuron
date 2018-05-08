import re
import string


class Case:
    def __init__(self, number, status, title, body):
        self.number = number
        self.status = status
        self.title = title
        self.body = body


printable = set(string.printable)


def remove_tags(text):
    pattern = re.compile('<.*?>')
    return re.sub(pattern, '', str(text))


def remove_junk(text, title):
    junk = ['License type: Pro', 'License type: Free', '1.* What happened',
            '2.* How .* reproduce it using the example you attached', 'Public status: Public',
            '\n', '\t', '\r', '\s+']
    text = text.replace(title, '')
    for pattern in junk:
        text = re.sub(re.compile(pattern), ' ', text)
    return text


def get_status(status):
    if status == "Bug":
        return "bug"
    elif status == "QA Incoming Incident":
        return "incident"
    else:
        return "?"


def clean(case):
    title = remove_tags(case.sOriginalTitle)
    body = remove_tags(case.events.event.s)
    body = remove_junk(body, title)
    filter(lambda x: x in printable, body)
    number = remove_tags(case.ixBug)
    status = remove_tags(case.sCategory)
    status = get_status(status)
    return Case(number, status, title, body)
