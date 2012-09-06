import re
from bs4 import BeautifulSoup

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

def scrape(html):
    _semester = re.compile('(Fall|Winter|Summer)')
    def _semester_or_course(tag):
        return ((tag.name == 'td' and tag.has_key('nowrap')) or
                (tag.name == 'b' and _semester.match(tag.text)))

    html = BeautifulSoup(html)
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
