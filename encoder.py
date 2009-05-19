"""XML2Dict: Convert xml file to python dict """

import re
try:
    import xml.etree.ElementTree as ET
except:
    import cElementTree as ET # for 2.4

__all__ = ['XML2Dict']

class XML2Dict(object):

    def __init__(self):
        pass

    def _parse_node(self, node):
        
        # tree dict
        tree = dict()

        # Save attributes
        for k, v in node.attrib.items():
            tree.update(self._make_dict(k, v))
        
        #Save childrens
        for child in node.getchildren():
            ctag = child.tag
            ctree = self._parse_node(child)
            if ctree == {}:
                #Save value
                cdict = self._make_dict(ctag, child.text.strip())
            else:
                cdict = self._make_dict(ctag, ctree)

            if ctag not in tree: # First time found
                tree.update(cdict)
                continue

            old = tree[ctag]
            if not isinstance(old, list):
                tree[ctag] = [old] # Multi entries, change to list

            tree[ctag].append(ctree) # Add new entry

        return  tree

    def _make_dict(self, tag, value):
        """Generate a new dict with tag and value
        
        If tag is like '{http://cs.sfsu.edu/csc867/myscheduler}patients',
        split it first to: http://cs.sfsu.edu/csc867/myscheduler, patients
        """
        result = re.compile("\{(.*)\}(.*)").search(tag)
        if result:
            ns, tag = result.groups() # We have a namespace!
            
            return {tag: value, ns: ns}
        
        return {tag: value}

    def fromstring(self, s):
        """Parse xml string to dict"""
        tmp = ET.fromstring(s)
        
        return self._make_dict(tmp.tag, self._parse_node(tmp))

if __name__ == '__main__':
    s = """<rss version="2.0"> 
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
 
	<link>http://www.twinsenliang.net/skill/20090413.html</link> 
 
	<title><![CDATA[this is the first title]]></title> 
 
	<author><![CDATA[twinsenliang@gmail.com(TwinsenLiang)]]></author> 
 
	<category><![CDATA[skill]]></category> 
 
	<pubDate>Mon, 13 Apr 2009 02:04:52 +0800</pubDate> 
 
	<guid>http://www.twinsenliang.net/skill/20090413.html</guid> 
 
	<description><![CDATA[this is the first content]]></description> 
 
</item> 
 
<item> 
 
	<link>http://www.twinsenliang.net/skill/20090409.html</link> 
 
	<title><![CDATA[this is the second title]]></title> 
 
	<author><![CDATA[twinsenliang@gmail.com(TwinsenLiang)]]></author> 
 
	<category><![CDATA[skill]]></category> 
 
	<pubDate>Thu, 09 Apr 2009 09:43:20 +0800</pubDate> 
 
	<guid>http://www.twinsenliang.net/skill/20090409.html</guid> 
 
	<description><![CDATA[this is the second content]]></description> 
 
</item> 
</channel>
</rss>"""

    xml = XML2Dict()
    rs = xml.fromstring(s)
    print(rs)