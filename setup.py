#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
#import sys

#from setuptools import setup, find_packages

#setup(
#    name = "bar-coordinator",
#    author = "d-elz",
#    author_email = "kwspoul@gmail.com",
#    description = ("A broadcast anonymity network"),
#
#    packages = find_packages(),
#

#    install_requires = [
        #'setuptools',
        #'PyCrypto',
        #'Twisted',
#        'argparse',
        #'pyptlib >= 0.0.5'
#        'pysocks'
#        ],
#)


con = lite.connect('bar0/db/bar0.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE ActiveList(id INTEGER PRIMARY KEY AUTOINCREMENT, special_id INT, ip INT, bridge_pk TEXT)")
    cur.execute("CREATE TABLE PublicList(id INTEGER PRIMARY KEY AUTOINCREMENT, nym TEXT, pk TEXT, signature TEXT)")
