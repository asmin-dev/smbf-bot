#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# author: zettamus
# github: zettamus

import requests
import base64
class Browser:
    def __init__(self):
        self.__req = requests.get
        self.__post = requests.post
        self.__cookies = {"cookie": None}
        self.__host = "https://free.facebook.com"
    @property
    def setkuki(self):
        pass
    @setkuki.setter
    def setkuki(self, kuki):
        self.__cookies = {"cookie": base64.b64decode(kuki).decode()}
    @setkuki.getter
    def showkuki(self):
        return self.__cookies
    def get(self,url):
        if self.__cookies["cookie"] == None:
            raise ValueError("Please set your cookie!")
        return self.__req(self.__host + url, cookies = self.__cookies)
    def post(self, url, data):
        if self.__cookies["cookie"] == None:
            raise ValueError("Please set your cookie!")
        return self.__post(self.__host + url, data = data, cookies = self.__cookies)



