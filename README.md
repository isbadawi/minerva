minerva
=======

This is a little python library that makes it easier for McGill
students to programmatically access information from Minerva. As of this
writing, it only supports retrieving unofficial transcript information.

You need a McGill ID and PIN (or McGill email and password) to access
Minerva. You can pass these in to the `login()` function, or set the
`MINERVA_USER` and `MINERVA_PASS` environment variables (you still need to call
`login()` if you do this).

```python
>>> import minerva
>>> isbadawi = minerva.login()
```

This retrieves your unofficial transcript.

```python
>>> transcript = isbadawi.transcript()
>>> import pprint
>>> pprint.pprint(transcript.get_courses())
[<Course: COMP 531 - Advanced Theory of Computation>,
<Course: COMP 547 - Cryptography & Data Security>,
... snip ...]
```

This transcript object can be queried to get courses satisfying certain
properties. You can search by semester, course title, section, grade,
average, or number of credits. For instance, this gets all Fall 2009 MATH
courses in which I got an A:

```python
>>> courses = transcript.get_courses(semester='Fall 2009',
                                     subject='MATH', grade='A')
>>> pprint.pprint(courses)
[<Course: MATH 235 - Algebra 1>,
<Course: MATH 318 - Mathematical Logic>]
```

Some useful bits:

```python
# What grade did I get in MATH317?
>>> transcript.get_courses(subject='MATH317')[0].grade
u'A'
```

```python
# Has the grade for COMP762 been posted yet?
>>> transcript.get_courses(subject='COMP762')[0].grade is not None
False
```

Installation
------------

To install `minerva`, simply: 

```bash
$ pip install mcgill-minerva
```

Note that one of the requirements is `lxml`, whose installation is sometimes
troublesome because it depends on `libxml` and `libxslt`. For more detailed
instructions regarding this, refer to [the `lxml` website](http://lxml.de/installation.html).
