import itertools

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

    def get_courses(self, **kwargs):
        return [course for course in self.courses if course.matches(**kwargs)]


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

    def matches(self, subject='', title='', grade='',
                average='', credits=None):
        return (subject.lstrip().lower() in self.subject.lstrip().lower() and
                title.lower() in self.title.lower() and
                (not grade or grade.upper() == self.grade) and
                (not average or average.upper() == self.average) and
                (credits is None or abs(credits - self.credits) < 0.001))


def scrape(html):
    terms = ['Fall', 'Winter', 'Summer']

    def is_semester(tag):
        return tag.name == 'b' and any(tag.text.startswith(t) for t in terms)

    def is_course(tag):
        return (tag.name == 'tr' and any(
            hasattr(c, 'name') and c.name == 'td' and c.has_attr('nowrap')
            for c in tag.children))

    html = bs4.BeautifulSoup(html)
    tags = html.find_all(lambda tag: is_semester(tag) or is_course(tag))
    semesters = [i for i, tag in enumerate(tags) if is_semester(tag)]
    term_gpas = [t.parent.parent.next_sibling.next_sibling.span.text
                 for t in html.find_all(text="TERM GPA:")]
    cum_gpas = [t.parent.parent.next_sibling.next_sibling.span.text
                for t in html.find_all(text="CUM GPA:")]
    transcript = []
    for i, index in enumerate(semesters):
        semester = tags[index].text.replace(u'\xa0', u' ')
        gpa = term_gpas[i] if i < len(term_gpas) else None
        cum_gpa = cum_gpas[i] if i < len(cum_gpas) else None
        raw_courses = [
            [t.get_text() for t in tag.find_all('td') if t.get_text()]
            for tag in itertools.takewhile(is_course, tags[index + 1:])
        ]
        courses = []
        just_saw_k = False
        for c in raw_courses:
            if just_saw_k:
                courses[-1].grade += ' (%s)' % c[6]
                just_saw_k = False
                continue
            course = Course(
                subject=c[1].encode('ascii', errors='ignore'),
                section=c[2].encode('utf-8'),
                title=c[3].encode('utf-8'),
                credits=float(c[4]),
                grade=c[6].encode('utf-8') if c[6] != u'\xa0' else None,
                average=c[10].encode('utf-8') if c[10] != u'\xa0' else None)
            courses.append(course)
            just_saw_k = course.grade == 'K'
        transcript.append(Term(semester=semester, courses=courses,
                               gpa=gpa, cum_gpa=cum_gpa))
    return Transcript(transcript)
