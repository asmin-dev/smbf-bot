#!/usr/bin/env python3
# Author: zettamus
# Github: asmin-dev
# Facebook : fb.me/zettid.1 
# telegram : t.me/zettamus
from bs4 import BeautifulSoup as bs
import re

class  Main:
    def __init__(self):
        self.id = []
        self.parser = None
    @property
    def browser(self):
        pass
    @browser.setter
    def browser(self, ses):
        self.parser = ses
    # get users from your friends list and from other users
    def friendlist(self,link):
        try:
            raw = bs(self.parser.get(link).content,'html.parser')
            users = re.findall('middle"><a class=".." href="(.*?)">(.*?)</a>',str(raw))
            for user in users:
                if "profile" in str(user[0]):
                    self.id.append(user[1] + "|" + re.findall('=(\d*)',str(user[0]))[0])
                elif "friend" in str(user):
                    continue
                else:
                    self.id.append(user[1] + "|" + user[0].replace("?","").replace('fref=fr_tab',''))
            if "Lihat Teman Lain" in str(raw):
                self.friendlist(raw.find("a",string="Lihat Teman Lain")["href"])
            return self.id 
        except:
            return self.id 
    
    # GET USER FROM USER REACTED ON POST
    def likes(self,url):
        try:
            raw = self.parser.get(url)
            users = re.findall('class="b."><a href="(.*?)">(.*?)</a></h3>',str(raw))                                   
            for user in users:
                if 'profile' in user[0]:
                    self.id.append(user[1] + "|" + re.findall("=(\d*)",str(user[0]))[0])
                else:
                    self.id.append(user[1] + "|" + user[0].split('/')[1])
                print(f'\r# {str(len(self.id))} retrieved',end="")
            if 'Lihat Selengkapnya' in str(raw):
                self.likes(raw.find('a',string="Lihat Selengkapnya")["href"])
            return self.id 
        except:
            return self.id 
    # GET USER FROM SEARCH
    def bysearch(self,url):
        try:
            search = self.parser.get(url)
            users = re.findall('profile picture".*?<a href="/(.*?)"><div class=".."><div.*?>(.*?)</div>',str(search))
            for user in users:
                if "profile" in user[0]:
                    self.id.append(user[1] + "|" + re.findall("=(\d*)",str(user[0]))[0])
                else:
                    self.id.append(user[1] + "|" + user[0].split("?")[0])
                print(f"\r# {str(len(self.id))} retrieved ",end="")
            if "Lihat Hasil Selanjutnya" in str(search):
                self.bysearch(search.find("a",string="Lihat Hasil Selanjutnya")["href"].split("book.com")[1])
            return self.id 
        except:
            return self.id

    def fromGrub(self,url):
        try:
            grab = self.parser.get(url)
            users = re.findall('a class=".." href="/(.*?)">(.*?)</a>',str(grab))
            for user in users:
                if "profile" in user[0]:
                    self.id.append(user[1] + "|" + re.findall('id=(\d*)',str(user[0]))[0])
                else:
                    self.id.append(user[1] + "|" + user[0])
                print(f"\r# {str(len(self.id))} retrieved ",end="")
            if "Lihat Selengkapnya" in str(grab):
                self.fromGrub(grab.find("a",string="Lihat Selengkapnya")["href"])
            return self.id 
        except:
            return self.id 
    def hashtag(self,url):
        try:
            grab = self.parser.get(url)
            users = re.findall('<h3.*?<strong><a href="/(.*?)__tn__=C">(.*?)</a>',str(grab))
            for user in users:
                if "profile" in user[0]:
                    self.id.append(user[1] + "|" + re.findall('id=(\d*)',str(user[0]))[0])
                else:
                    self.id.append(user[1] +"|" + user[0].replace("?",""))
                print(f"\r# {str(len(self.id))} retrieved ",end="")
            if len(self.id) != 0:
                if "Lihat Hasil Selanjutnya" in str(grab):
                    self.hashtag(grab.find("a",string="Lihat Hasil Selanjutnya")["href"].replace("https://free.facebook.com",""))
            return self.id 
        except:
            return self.id 
