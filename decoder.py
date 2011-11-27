#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Dict2XML: Convert python dict to xml string

@author: Mc.Spring
@contact: Heresy.Mc@gmail.com
@since: Created on 2009-5-18
@todo: Add namespace support
@copyright: Copyright (C) 2009 MC.Spring Team. All rights reserved.
@license: http://www.apache.org/licenses/LICENSE-2.0 Apache License
'''
import sys
try:
    import xml.etree.ElementTree as ET
except:
    import cElementTree as ET # for 2.4

__all__ = ['Dict2XML']

class Dict2XML(object):

    def __init__(self, coding='UTF-8'):
        self._root = None
        self._coding = coding

    def _parse_dict(self, edict, etree=None):
        tree = None

        for tag, value in edict.items():
            if etree is not None and isinstance(value, list):
                # children nodes
                elist = [self._parse_dict({tag: item}) for item in value]
                for et in elist:
                    etree.append(et)

                del elist
                continue

            elif etree is None and '@'==tag[:1]:
                # tree's attributes
                etree = tree

            tree = self._make_xml(tag, value, etree)

        return tree

    def _make_xml(self, tag, value, parent):
        """Generate a new xml from the dict key and value
        
        The parent param is ET object
        """
        if '@'==tag[:1] and isinstance(value, dict):
            tag = tag[1:]

            if parent is None:
                if self._root is None:
                    el = ET.Element(tag, value)
                    self._root = el
                else:
                    el = self._root
                    self._root = None

            else:
                el = parent if tag==parent.tag else parent.find(tag)
                if el is None:
                    # Element first add
                    el = ET.SubElement(parent, tag, value)
                else:
                    # Save attributes
                    el.attrib.update(value)

            return el

        stag = '#'+tag
        if stag in value:
            if isinstance(value[stag], dict):
                el = ET.Element(tag, value[stag])
            else:
                el = ET.Element(tag)

            del value[stag]

        else:
            if parent is None:
                if self._root is None:
                    el = ET.Element(tag)
                    self._root = el
                else:
                    el = self._root
                    self._root = None

            else:
                el = parent.find(tag)
                if el is None:
                    # Element first add
                    el = ET.SubElement(parent, tag)

        if isinstance(value, dict):
            self._parse_dict(value, el)
        else:
            el.text = value     

        return el

    def parse(self, dict):
        """Parse dict to xml string
        
        @attention: every dict must have a root key!
        """
        return ET.tostring(self._parse_dict(dict))


if __name__ == '__main__':
    test = {'one': {'@class': {'id': 'test'}},
            'two': {'class': {'student': [{'age': '24', '#student': 'type', 'name': 'thiru'},
                                          {'age': '28', '#student': {'id': '5678'}, 'name': 'bharath'}]},
                    '@class': {'id': 'test'}},
            'three': {'@rss': {'version': '2.0', 'author': 'Mc.Spring'},
                      'rss': {'channel': {'language': 'en-us',
                                          'link': 'https://github.com/mcspring', 
                                          'description': "Hello,world.", 
                                          'copyright': 'Copyright 2011-2012 Spring Mc. All rights reserved.', 
                                          'title': 'Spring Mc', 
                                          'item': [{'category': 'skill', 'guid': 'https://github.com/mcspring/googl.go', 'link': 'https://github.com/mcspring/googl.go', '@link': {'target': '_blank'}, 'pubDate': 'Mon, 13 Apr 2011 02:04:52 +0800', 'author': 'Heresy.Mc@gmail.com(Spring Mc)', 'title': 'This is googl.go proejct', 'description': 'This is the first project written in go, thanks!'}, 
                                                   {'category': 'skill', 'guid': 'https://github.com/mcspring/XML2Dict', 'link': 'https://github.com/mcspring/XML2Dict', '@link':{'target': '_blank'}, 'pubDate': 'Mon, 15 Apr 2009 02:04:52 +0800', 'author': 'Heresy.Mc@gmail.com(Spring Mc)', 'title': 'This is XML2Dict project', 'description': 'This is the first project written in python, thanks!'}], 
                                          'image': {'url': 'https://github.com/mcspring/logo.gif', 'link': 'https://github.com/mcspring/', 'description': 'Spring Mc', 'title': 'Spring on github'}, 
                                          'generator': 'XmlSave 2.0', 
                                          'webMaster': 'Heresy.Mc@gmail.com(Spring)'}}},
            'four': {'person': {'age': '', 'name': 'spring', 'address': ''}},
            'five': {'doc': {'x': [{'#x': {'a': '1'}}, {'#x': {'a': '2'}}]}}
            }
    
    for item in test:
        obj = Dict2XML()
        
        print(obj.parse(test[item]))
        print
