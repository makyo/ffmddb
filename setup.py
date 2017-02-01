#!/usr/bin/env python

from setuptools import (
    find_packages,
    setup,
)


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='ffmddb',
    version='0.0.0',
    description='A flat-file-with-metadata database.',
    long_description=long_description,
    author='Madison Scott-Clary',
    author_email='makyo@drab-makyo.com',
    install_requires=['pyyaml'],
    packages=find_packages(),
    setup_requires=['nose>=1.0', 'flake8', 'six'],
    tests_require=['nose', 'coverage', 'mock'],
    entry_points={
        'console_scripts': [
            'ffmddb-client = ffmddb.client:run',
            'ffmddb-server = ffmddb.server:run',
        ],
    },
    url='https://github.com/makyo/prose-wc',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Database :: Front-Ends',
    ])
