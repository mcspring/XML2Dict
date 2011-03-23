#!/usr/bin/env python
# -*- conding=utf-8 -*-

from distutils.core import setup

setup(name='XML2Dict',
    version='0.1',
    author='Spring Mc',
    author_email='Heresy.Mc@gmail.com',
    packages=['encoder', 'decoder'],
    url='https://github.com/mcspring/XML2Dict',
    license='http://www.apache.org/licenses/LICENSE-2.0.html',
    description='Convert between XML String and Python Dict',
    long_description=open('README.md').read())
