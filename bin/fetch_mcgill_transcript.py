#!/usr/bin/env python
import argparse
import getpass
import sys
import StringIO

import minerva


def parse_args():
    parser = argparse.ArgumentParser(
        description='fetch McGill transcript',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-a', '--auth', help='''email:password or sid:pin
If the password (or pin) is omitted, will prompt for them.
If the argument is omitted altogether, will look to the values of the
MINERVA_USER and MINERVA_PASS environment variables.
''')
    return parser.parse_args()


def get_user_credentials():
    args = parse_args()
    if args.auth is None:
        return None, None
    if ':' in args.auth:
        return args.auth.split(':', 1)
    try:
        password = getpass.getpass("Password for user '%s': " % args.auth)
    except (EOFError, KeyboardInterrupt):
        sys.stderr.write('\n')
        sys.exit(0)
    return args.auth, password


# TODO(isbadawi): maybe extract some of the logic here to work on
# generic tabular data (as e.g. lists of lists)?
def format_transcript(transcript):
    def term_key(term):
        semester, year = term.semester.split()
        return year, {'Winter': 0, 'Summer': 1, 'Fall': 2}[semester]

    buf = StringIO.StringIO()
    longest_subject_len = max(len(course.subject)
                              for course in transcript.get_courses())
    longest_title_len = max(len(course.title)
                            for course in transcript.get_courses())
    for term in sorted(transcript.terms.values(), key=term_key):
        buf.write(term.semester)
        if term.gpa is not None and term.cum_gpa is not None:
            buf.write(' (GPA: %s, cumulative: %s)' % (term.gpa, term.cum_gpa))
        buf.write('\n')
        for course in term.courses:
            buf.write('\t')
            buf.write('\t'.join([
                course.subject.ljust(longest_subject_len),
                course.title.ljust(longest_title_len),
                str(course.credits),
                (course.grade or '').ljust(2),
                (course.average or '').ljust(2)]))
            buf.write('\n')
    return buf.getvalue()


def main():
    username, password = get_user_credentials()
    client = minerva.login(username, password)
    transcript = client.transcript()
    print format_transcript(transcript)

if __name__ == '__main__':
    main()
