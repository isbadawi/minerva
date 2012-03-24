import re
from bs4 import BeautifulSoup
from common import browser, urls
from util import cached

_whitespace = re.compile(r'\s+')
def _no_whitespace(s):
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
def _get_transcript():
    _semester = re.compile('(Fall|Winter|Summer)')
    def _semester_or_course(tag):
        return ((tag.name == 'td' and tag.has_key('nowrap')) or
                (tag.name == 'b' and _semester.match(tag.text)))

    html = BeautifulSoup(browser.open(urls['transcript']))
    all_courses = html.find_all(_semester_or_course)
    semesters = [t.parent for t in html.find_all(text=_semester)][2:]
    indices = [all_courses.index(t) for t in semesters]
    term_gpas = [t.parent.parent.next_sibling.next_sibling.span.text 
                for t in html.find_all(text="TERM GPA:")]
    cum_gpas = [t.parent.parent.next_sibling.next_sibling.span.text 
                for t in html.find_all(text="CUM GPA:")]
    transcript = []
    for i, (index, semester) in enumerate(zip(indices, semesters)):
        semester = semester.text.replace(u'\xa0', u' ')
        next = indices[i+1] if i < len(indices) - 1 else len(all_courses)
        courses = [
            [t.get_text() for t in all_courses[j:j+11] if t.get_text()]
            for j in range(index+1, next, 11)
        ]
        courses = [_build_course(c) for c in courses]
        gpa = term_gpas[i] if i < len(term_gpas) else None
        cum_gpa = cum_gpas[i] if i < len(cum_gpas) else None
        transcript.append({
            'semester': semester,
            'courses': courses,
            'gpa': gpa,
            'cum_gpa': cum_gpa,
        })
    return transcript

def get(**kwargs):
    """
    Query the unofficial transcript. Call with no arguments to get the 
    whole transcript, or specify keyword arguments to narrow down the
    results. Note that if you specify multiple keyword arguments, they are
    ANDed together -- for OR, you should call get several times, together
    with e.g. list.extend.
    """
    matches = _get_transcript()
    semester = kwargs.get('semester', None)
    if semester is not None:
        matches = next(m['courses'] for m in matches if m['semester'] == semester)
    elif kwargs:
        matches = sum((m['courses'] for m in matches), [])
    subject = kwargs.get('subject', None)
    if subject is not None:
        subject = _no_whitespace(subject.lower())
        matches = [m for m in matches if subject in _no_whitespace(m['subject'].lower())]
    title = kwargs.get('title', None)
    if title is not None:
        title = title.lower()
        matches = [m for m in matches if title in m['title'].lower()]
    grade = kwargs.get('grade', None)
    if grade is not None:
        grade = grade.lower()
        matches = [m for m in matches if m['grade'] is not None and grade == m['grade'].lower()]
    average = kwargs.get('average', None)
    if average is not None:
        average = average.lower()
        matches = [m for m in matches if m['average'] is not None and average == m['average'].lower()]
    credits = kwargs.get('credits', None)
    if credits is not None:
        credits = int(credits, 10)
        matches = [m for m in matches if credits == m['credits']]
    return matches
