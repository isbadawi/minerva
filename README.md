python-mcgill
=============

This is a little (growing) python library that makes it easier for McGill
students to programmatically access information from Minerva.

Here's an example:

    >>> import mcgill
    >>> mcgill.login()
    # all COMP courses in which I got an A
    >>> comp_As = mcgill.courses.get(grade='A', subject='COMP')
    >>> from pprint import pprint
    >>> pprint(comp_As)
    [{'average': u'B',
      'credits': 3,
      'grade': u'A',
      'section': u'001',
      'subject': u'COMP 250',
      'title': u'Intro to Computer Science'},
    ... snip ...
    ]

You need a McGill ID and PIN (or McGill email and password) to access
Minerva. You can pass these in to the `login()` function, or set the
`MCGILL_SID` and `MCGILL_PIN` environment variables (you still need to call
`login()` if you do this).
