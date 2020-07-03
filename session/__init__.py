#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: zettamus


from . import session, parsing
import re

class Account:
    def __init__(self):
        self.__id = None
        self.__name = None
        self.__username = None
        self.__profile_pic = None
        self.__login = False
    def __str__(self,ses):
        data = ses.get("/me").content
        if "mbasic_logout_button" in str(data):
            user = parsing.parsing(data).find_all("a")
            photos = parsing.parsing(data).find_all("img")
            self.__name = parsing.parsing(data).find("title").text
            try:
                self.__id = re.findall('/(\d*)/allactivity', str(data))[0]
            except:
                pass
            try:
                for link in user:
                    if "friends?lst" in str(link):
                        self.__username = re.findall('/(.*?)/fr',str(link["href"]))[0]
            except:
                pass
            for profile in photos:
                if "profile picture" in str(profile):
                    self.__profile_pic = profile["src"]
                    break
            return {"name": self.__name, "id": self.__id, "username":self.__username, "profile_pic": self.__profile_pic}
        else:
          return False

    @property
    def logged(self):
        return self.__login
    def loged(self):
        self.__login = False
    def login(self,ses):
        if 'mbasic_logout_button' in str()ses.get("/me").content):
            return True
