#!/usr/bin/python

from copyfromnet import *

jm = (Jenkins("http://127.0.0.1:8080",username='wayne',password='123456'))
print (jm.create_view('TESTB',EMPTY_VIEW_CONFIG_XML))
