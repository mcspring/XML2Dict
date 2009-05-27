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

import re
try:
    import xml.etree.ElementTree as ET
except:
    import cElementTree as ET # for 2.4

__all__ = ['Dict2XML']

class Dict2XML(object):

    def __init__(self, coding='UTF-8'):
        self._root = None
        self._coding = coding

    def _parse_dict(self, dict, et=None):
        
        tree = None
        for k, v in dict.items():
            if isinstance(v, list):
                _list = [self._parse_dict({k: item}) for item in v]
                for _et in _list:
                    et.append(_et)
                
                del _list
                continue
            
            tree = self._make_xml(k, v, et)
        
        return tree

    def _make_xml(self, tag, value, parent):
        """Generate a new xml from the dict key and value
        
        The parent param is ET object
        """        
        # Parse tag attributes
        attri = {}
        if ('@' == tag[:1]) and isinstance(value, dict):
            tag = tag[1:]
            attri.update(value)
        
        if parent is None:
            if self._root is not None:
                el = self._root
                self._root = None
            else:
                el = ET.Element(tag, attri)
                self._root = el
        else:
            _el = parent.find(tag)
            if _el is None: # Element first add
                el = ET.SubElement(parent, tag, attri)
            else:
                el = _el
                if attri != {}:
                    # Save attributes
                    el.attrib.update(attri)
        
        if attri != {}:
            return

        if isinstance(value, dict):
            self._parse_dict(value, el)
        else:
            el.text = value

        return el
    
    def parse(self, dict):
        """Parse dict to xml string"""
        return ET.tostring(self._parse_dict(dict))

if __name__ == '__main__':
    d = {
    "@rss": {
        "version": "2.0",
        "author": "Mc.Spring"
    },
    "rss": {
        "channel": {
            "language": "zh-cn",
            "link": "http://www.twinsenliang.net",
            "description": "je m' appelle twinsen.",
            "copyright": "Copyright 2000-2009 Twinsen Liang all rights reserved",
            "title": "Twinsen Liang",
            "item": [
                {
                    "category": "skill",
                    "guid": "http://www.twinsenliang.net/skill/20090413.html",
                    "link": "http://www.twinsenliang.net/skill/20090413.html",
                    "@link": {
                        "target": "_blank"
                    },
                    "pubDate": "Mon, 13 Apr 2009 02:04:52 +0800",
                    "author": "twinsenliang@gmail.com(TwinsenLiang)",
                    "title": "This is the first article title",
                    "description": "This is the first article content, thanks!"
                },
                {
                    "category": "skill",
                    "guid": "http://www.twinsenliang.net/skill/20090414.html",
                    "link": "http://www.twinsenliang.net/skill/20090414.html",
                    "@link": {
                        "target": "_blank"
                    },
                    "pubDate": "Mon, 15 Apr 2009 02:04:52 +0800",
                    "author": "twinsenliang@gmail.com(TwinsenLiang)",
                    "title": "This is the second article title",
                    "description": "This is the second article content, thanks!"
                }
            ],
            "image": {
                "url": "http://www.twinsenliang.net/logo.gif",
                "link": "http://www.twinsenliang.net/",
                "description": "Twinsen Liang",
                "title": "Twinsen Liang"
            },
            "generator": "TXmlSave 2.0",
            "webMaster": "twinsenliang@gmail.com(twinsen)"
        }
    }
}

    obj = Dict2XML()
    rs = obj.parse(d)
    print(rs)