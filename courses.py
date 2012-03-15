import re
from bs4 import BeautifulSoup
from common import browser, urls
from util import cached

_whitespace = re.compile(r'\s+')
def no_whitespace(s):
    return _whitespace.sub('', s)

def _build_course(raw_course):
    return {
        'subject': raw_course[1],
        'section': raw_course[2],
        'title': raw_course[3],
        'credits': int(raw_course[4]),
        'grade': raw_course[6] if raw_course[6] != u'\xa0' else None,
        'average': raw_course[10] if raw_course[10] != u'\xa0' else None,
    }

@cached
def transcript():
    html = BeautifulSoup(browser.open(urls['transcript']))
    courses = html.find_all('td', attrs={'nowrap': ''})
    courses = [
        [t.get_text() for t in courses[i:i+11] if t.get_text()] 
        for i in range(0, len(courses), 11)
    ]
    courses = [_build_course(raw_course) for raw_course in courses]
    return courses

def get(subject=None, title=None, grade=None, average=None, credits=None):
    matches = transcript()
    if subject is not None:
        subject = no_whitespace(subject)
        matches = [m for m in matches if subject in no_whitespace(m['subject'].lower())]
    if title is not None:
        title = title.lower()
        matches = [m for m in matches if title in m['title'].lower()]
    if grade is not None:
        grade = grade.lower()
        matches = [m for m in matches if m['grade'] is not None and grade == m['grade'].lower()]
    if average is not None:
        average = average.lower()
        matches = [m for m in matches if m['average'] is not None and average == m['average'].lower()]
    if credits is not None:
        credits = int(credits, 10)
        matches = [m for m in matches if credits == m['credits']]
    return matches
