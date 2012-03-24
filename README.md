python-mcgill
=============

This is a little (growing) python library that makes it easier for McGill
students to programmatically access information from Minerva.


    >>> import mcgill

You need a McGill ID and PIN (or McGill email and password) to access
Minerva. You can pass these in to the `login()` function, or set the
`MCGILL_SID` and `MCGILL_PIN` environment variables (you still need to call
`login()` if you do this).

    >>> mcgill.login()

Let's start with a simple example. This retrieves your unofficial 
transcript.

    >>> courses = mcgill.transcript.get()
    >>> import pprint
    >>> pprint.pprint(courses)
    [{'courses': [{'average': u'B',
                   'credits': 3,
                   'grade': u'A',
                   'section': u'001',
                   'subject': u'COMP 250',
                   'title': u'Intro to Computer Science'},
                   ... snip ...],
      'cum_gpa': u'3.88',
      'gpa': u'3.88',
      'semester': u'Fall 2009'},
      ... snip ...]

`get()` takes a few keyword arguments to narrow down the results. For
instance, what if I wanted a list of all MATH courses in which I got an A?

    >>> results = mcgill.transcript.get(subject='MATH', grade='A')
    >>> pprint.pprint(results)
    [{'average': u'B-',
      'credits': 3,
      'grade': u'A',
      'section': u'001',
      'subject': u'MATH 235',
      'title': u'Algebra 1'},
    ... snip ...
    ]

Or maybe I'm just looking to see if the grade was released for a certain
course...

    >>> results = mcgill.transcript.get(title='games')
    >>> pprint.pprint(results)
    [{'average': None,
      'credits': 4, 
      'grade': None, 
      'section': u'001'
      'subject': u'COMP 521',
      'title': u'Modern Computer Games'}]
