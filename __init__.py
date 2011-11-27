#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
XML2Dict: Convert xml and python dict

@since: Created on 2009-5-18
@author: Mc.Spring
@contact: Heresy.Mc@gmail.com
@copyright: Copyright (C) 2009 MC.Spring Team. All rights reserved.
@license: http://www.apache.org/licenses/LICENSE-2.0 Apache License
'''

__version__ = '0.2.1'
__all__ = [
    'parsexml', 'parsedict',
    'XML2Dict', 'Dict2XML',
]

__author__ = 'Mc.Spring <Heresy.Mc@gmail.com>'


from encoder import XML2Dict
from decoder import Dict2XML


def parsexml(s, cls = None):
    if cls is None:
        cls = XML2Dict

    return cls().parse(s)


def parsedict(d, cls = None):
    if cls is None:
        cls = Dict2XML

    return cls().parse(d)
