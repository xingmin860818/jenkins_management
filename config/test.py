#!/usr/bin/python env

import xml.dom.minidom
dom = xml.dom.minidom.parse('view.xml')

root = dom.documentElement
print(root)
print(root.getElementsByTagName('jobNames'))
print(root.childNodes)
