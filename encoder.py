#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
XML2Dict: Convert xml string to python dict

@author: Mc.Spring
@contact: Heresy.Mc@gmail.com
@since: Created on 2009-5-18
@todo: Add namespace support
@copyright: Copyright (C) 2009 MC.Spring Team. All rights reserved.
@license: http://www.apache.org/licenses/LICENSE-2.0 Apache License
'''

try:
    import xml.etree.ElementTree as ET
except:
    import cElementTree as ET # for 2.4


__all__ = ['XML2Dict']


class XML2Dict(object):

    def __init__(self, coding='UTF-8'):
        self._coding = coding

    def _parse_node(self, node):
        tree = {}

        #Save childrens
        for child in node.getchildren():
            ctag = child.tag
            cattr = child.attrib
            ctext = child.text.strip().encode(self._coding) if child.text is not None else ''
            ctree = self._parse_node(child)

            if not ctree:
                cdict = self._make_dict(ctag, ctext, cattr)
            else:
                cdict = self._make_dict(ctag, ctree, cattr)

            if ctag not in tree: # First time found
                tree.update(cdict)
                continue

            atag = '@' + ctag
            atree = tree[ctag]
            if not isinstance(atree, list):
                if not isinstance(atree, dict):
                    atree = {}

                if atag in tree:
                    atree['#'+ctag] = tree[atag]
                    del tree[atag]

                tree[ctag] = [atree] # Multi entries, change to list

            if cattr:
                ctree['#'+ctag] = cattr

            tree[ctag].append(ctree)

        return  tree

    def _make_dict(self, tag, value, attr=None):
        '''Generate a new dict with tag and value
        
        If attr is not None then convert tag name to @tag
        and convert tuple list to dict
        '''
        ret = {tag: value}

        # Save attributes as @tag value
        if attr:
            atag = '@' + tag

            aattr = {}
            for k, v in attr.items():
                aattr[k] = v

            ret[atag] = aattr

            del atag
            del aattr

        return ret

    def parse(self, xml):
        '''Parse xml string to python dict
        
        '''
        EL = ET.fromstring(xml)

        return self._make_dict(EL.tag, self._parse_node(EL), EL.attrib)



if __name__ == '__main__':
    test = {'one': '''<rss author="Mc.Spring" version="2.0">
    <channel>
        <description>je m' appelle twinsen.</description>
        <copyright>Copyright 2000-2009 Twinsen Liang all rights reserved</copyright>
        <title>Twinsen Liang</title>
        <language>zh-cn</language>
        <image>
            <url>http://www.twinsenliang.net/logo.gif</url>
            <link>http://www.twinsenliang.net/</link>
            <description>Twinsen Liang</description>
            <title>Twinsen Liang</title>
        </image>
        <generator>TXmlSave 2.0</generator>
        <item>
            <category>skill</category>
            <description>This is the second article content, thanks!</description>
            <pubDate>Mon, 15 Apr 200902:04:52 +0800</pubDate>
            <author>twinsenliang@gmail.com(TwinsenLiang)</author>
            <title>This is the second article title</title>
            <link target="_blank">http://www.twinsenliang.net/skill/20090414.html</link>
            <guid>http://www.twinsenliang.net/skill/20090414.html</guid>
        </item>
        <item>
            <category>skill</category>
            <description>This isthe second article content, thanks!</description>
            <pubDate>Mon, 15 Apr 2009 02:04:52 +0800</pubDate>
            <author>twinsenliang@gmail.com(TwinsenLiang)</author>
            <title>This is the second article title</title>
            <link target="_blank">http://www.twinsenliang.net/skill/20090414.html</link>
            <guid>http://www.twinsenliang.net/skill/20090414.html</guid>
        </item>
        <link>http://www.twinsenliang.net</link>
        <webMaster>twinsenliang@gmail.com(twinsen)</webMaster>
    </channel>
</rss>''',
            'two': '''<class id="test">
    <student id="1234">
        <age>24</age>
        <name>thiru</name>
    </student>
    <student id="5678">
        <age>28</age>
        <name>bharath</name>
    </student>
</class>''',
            'three': '''<class id="test"></class>''',
            'four': '''<person>
    <name>spring</name>
    <age></age>
    <address />
</person>''',
            'five': '''<doc>
    <x a="1" />
    <x a="2" />
</doc>'''}

    for item in test:
        obj = XML2Dict(coding='utf-8')
        
        print(obj.parse(test[item]))
        print
