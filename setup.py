# -*- coding: utf-8 -*-
#
#  setup.py
#  simplestats
#

from setuptools import setup

VERSION = '0.2.1'

f = open('src/__version__.py', 'w')
f.write('# Autogenerated by setup.py\n')
f.write('version = "%s"\n' % VERSION)
f.close()

setup(
    name='simplestats',
    description="Simple statistics modules for data analysis.",
    long_description="""
    Provides basic statistics calcuations, frequency distributions, data
    approximation methods, and others.
    """,
    url="http://bitbucket.org/larsyencken/simplestats/",
    version=VERSION,
    author="Lars Yencken",
    author_email="lars@yencken.org",
    license="BSD",
    packages=['simplestats'],
)
