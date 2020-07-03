#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: zettamus

from bs4 import BeautifulSoup as parser

def parsing(html):
    return parser(html,"html.parser")
