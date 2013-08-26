from setuptools import setup

setup(
    name='mcgill-minerva',
    version='0.1.1',
    description='Client library for McGill Minerva.',
    url='https://github.com/isbadawi/minerva',
    author='Ismail Badawi',
    author_email='isbadawi@gmail.com',
    keywords='mcgill minerva',
    packages=['minerva'],
    scripts=['bin/fetch-mcgill-transcript'],
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
