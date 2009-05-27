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

    def __init__(self, coding = 'UTF-8'):
        self._coding = coding

    def _parse_node(self, node):
        
        # tree dict
        tree = dict()
        
        #Save childrens
        for child in node.getchildren():
            ctag = child.tag
            cattri = child.attrib
            ctree = self._parse_node(child)
            
            if ctree == {}:
                cdict = self._make_dict(ctag, child.text.encode(self._coding).strip(), cattri)
            else:
                cdict = self._make_dict(ctag, ctree, cattri)

            if ctag not in tree: # First time found
                tree.update(cdict)
                continue

            tmp = tree[ctag]
            if not isinstance(tmp, list):
                tree[ctag] = [tmp] # Multi entries, change to list

            tree[ctag].append(ctree) # Add new entry

        return  tree

    def _make_dict(self, tag, value, attri = None):
        """Generate a new dict with tag and value
        
        If attri is True then convert tag name to @tag
        and convert tuple list to dict
        """
        ret = {tag: value}
        
        # Save attributes as @tag value
        if attri:
            tmp = '@' + tag
            
            adict = {}
            for k, v in attri.items():
                adict[k] = v
            
            ret[tmp] = adict
            
            del tmp
            del adict
        
        return ret

    def parse(self, xml):
        """Parse xml string to dict"""
        EL = ET.fromstring(xml)
        
        return self._make_dict(EL.tag, self._parse_node(EL), EL.attrib)

if __name__ == '__main__':
    s = """<rss version="2.0" author="Mc.Spring"> 
<channel> 
<title><![CDATA[Twinsen Liang]]></title> 
<link>http://www.twinsenliang.net</link> 
<description><![CDATA[je m' appelle twinsen.]]></description> 
<language>zh-cn</language> 
<copyright><![CDATA[Copyright 2000-2009 Twinsen Liang all rights reserved]]></copyright> 
<webMaster><![CDATA[twinsenliang@gmail.com(twinsen)]]></webMaster> 
<generator>TXmlSave 2.0</generator> 
<image> 
	<title>Twinsen Liang</title> 
	<url>http://www.twinsenliang.net/logo.gif</url> 
	<link>http://www.twinsenliang.net/</link> 
	<description>Twinsen Liang</description> 
</image> 
<item> 
 
	<link target="_blank">http://www.twinsenliang.net/skill/20090413.html</link> 
 
	<title><![CDATA[This is the first article title]]></title> 
 
	<author><![CDATA[twinsenliang@gmail.com(TwinsenLiang)]]></author> 
 
	<category><![CDATA[skill]]></category> 
 
	<pubDate>Mon, 13 Apr 2009 02:04:52 +0800</pubDate> 
 
	<guid>http://www.twinsenliang.net/skill/20090413.html</guid> 
 
	<description><![CDATA[This is the first article content, thanks!]]></description> 
 
</item>
<item> 
 
    <link target="_blank">http://www.twinsenliang.net/skill/20090414.html</link> 
 
    <title><![CDATA[This is the second article title]]></title> 
 
    <author><![CDATA[twinsenliang@gmail.com(TwinsenLiang)]]></author> 
 
    <category><![CDATA[skill]]></category> 
 
    <pubDate>Mon, 15 Apr 2009 02:04:52 +0800</pubDate> 
 
    <guid>http://www.twinsenliang.net/skill/20090414.html</guid> 
 
    <description><![CDATA[This is the second article content, thanks!]]></description> 
 
</item>
</channel>
</rss>"""

	
    obj = XML2Dict(coding = 'gb2312')

    rs = obj.parse(s)

    print(rs)