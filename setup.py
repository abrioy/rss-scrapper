#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'PyYAML>=3.11',
    'requests>=2.13.0',
    'lxml>=3.7.3',
    'cssselect>=1.0.1',
    'feedgen>=0.5.1',
    'parsedatetime>=2.4',
    'pytz>=2017.2',
]

test_requirements = [

]

setup(
    name='rss_scrapper',
    version='0.1.0',
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    long_description=readme + '\n\n' + history,
    author="Antoine Brioy",
    author_email='antoine.brioy@gmail.com',
    url='https://github.com/abrioy/rss_scrapper',
    packages=[
        'rss_scrapper',
    ],
    package_dir={'rss_scrapper':
                 'rss_scrapper'},
    entry_points={
        'console_scripts': [
            'rss_scrapper=rss_scrapper.__main__:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='rss_scrapper',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
