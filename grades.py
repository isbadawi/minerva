from bs4 import BeautifulSoup
from common import browser, urls
from util import cached

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
