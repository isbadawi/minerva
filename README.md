python-mcgill
=============

This is a little python library that makes it easier for McGill
students to programmatically access information from Minerva. As of this
writing, it only supports retrieving unofficial transcript information.

You need a McGill ID and PIN (or McGill email and password) to access
Minerva. You can pass these in to the `login()` function, or set the
`MCGILL_SID` and `MCGILL_PIN` environment variables (you still need to call
`login()` if you do this).

    >>> import mcgill
    >>> isbadawi = mcgill.login()

This retrieves your unofficial transcript.

    >>> transcript = isbadawi.transcript
    >>> import pprint
    >>> pprint.pprint(transcript.get_courses())
    [<Course: COMP 531 - Advanced Theory of Computation>,
     <Course: COMP 547 - Cryptography & Data Security>,
     ... snip ...]

This transcript object can be queried to get courses satisfying certain
properties. You can search by semester, course title, section, grade,
average, or number of credits. For instance, this gets all Fall 2009 MATH
courses in which I got an A:

    >>> courses = transcript.get_courses(semester='Fall 2009',
                                         subject='MATH', grade='A')
    >>> pprint.pprint(courses)
    [<Course: MATH 235 - Algebra 1>,
     <Course: MATH 318 - Mathematical Logic>]
