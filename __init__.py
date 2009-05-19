'''
Created on 2009-5-18

@author: Administrator
'''
__version__ = '0.1.0'
__all__ = [
    'parsestring', 'XML2Dict',
]

__author__ = 'Mc.Spring <Heresy.Mc@gmail.com>'

from encoder import XML2Dict

def parsestring(s, cls = None):
    if cls is None:
        cls = XML2Dict

    return cls().fromstring(s)