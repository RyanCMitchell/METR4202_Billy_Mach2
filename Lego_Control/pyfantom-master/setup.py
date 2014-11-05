#!/usr/bin/env python

from distutils.core import setup

try:
    readme = open('README', 'r')
    ldesc = readme.read(8192)
    readme.close()
except:
    ldesc = ""

setup(
    name='pyfantom',
    version='0.1',
    author='Nicolas Schodet',
    author_email='nico@ni.fr.eu.org',
    description='Python Wrapper for LEGO Mindstorms NXT Fantom Driver',
    url='http://git.ni.fr.eu.org/?p=pyfantom.git;a=summary',
    license='Gnu GPL v2',
    py_modules=['pyfantom'],
    long_description=ldesc
)
