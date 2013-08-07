import re

import bs4

class Transcript(object):
    def __init__(self, terms):
        self.terms = {term.semester: term for term in terms}

    def get_courses(self, **kwargs):
        semester = kwargs.pop('semester', None)
        if semester is not None:
            return self.terms[semester].get_courses(**kwargs)
        return sum((term.get_courses(**kwargs)
                    for term in self.terms.values()), [])

class Term(object):
    def __init__(self, courses, cum_gpa, gpa, semester):
        self.courses = courses
        self.cum_gpa = cum_gpa
        self.gpa = gpa
        self.semester = semester

    def __repr__(self):
        return '<Term: %s>' % self.semester

    def get_courses(self, subject=None, title=None, grade=None,
                     average=None, credits=None):
        matches = self.courses
        if subject is not None:
            subject = _clean(subject)
            matches = [m for m in matches if subject in _clean(m.subject)]
        if title is not None:
            title = title.lower()
            matches = [m for m in matches if title in m.title.lower()]
        if grade is not None:
            grade = grade.upper()
            matches = [m for m in matches if grade == m.grade]
        if average is not None:
            average = average.upper()
            matches = [m for m in matches if average == m.average]
        if credits is not None:
            credits = int(credits, 10)
            matches = [m for m in matches if credits == m.credits]
        return matches

class Course(object):
    def __init__(self, average, credits, grade, section, subject, title):
        self.average = average
        self.credits = credits
        self.grade = grade
        self.section = section
        self.subject = subject
        self.title = title

    def __repr__(self):
        return '<Course: %s - %s>' % (self.subject, self.title)

_whitespace = re.compile(r'\s+')
def _clean(s):
    return _whitespace.sub('', s.lower())

def _build_course(raw_course):
    return Course(
        subject=raw_course[1],
        section=raw_course[2],
        title=raw_course[3],
        credits=int(raw_course[4]),
        grade=raw_course[6] if raw_course[6] != u'\xa0' else None,
        average=raw_course[10] if raw_course[10] != u'\xa0' else None,
    )

def scrape(html):
    _semester = re.compile('(Fall|Winter|Summer)')
    def _semester_or_course(tag):
        return ((tag.name == 'td' and tag.has_key('nowrap')) or
                (tag.name == 'b' and _semester.match(tag.text)))

    html = bs4.BeautifulSoup(html)
    all_courses = html.find_all(_semester_or_course)
    semesters = [t.parent for t in html.find_all(text=_semester)][1:]
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
        transcript.append(Term(semester=semester, courses=courses,
                               gpa=gpa, cum_gpa=cum_gpa))
    return Transcript(transcript)
