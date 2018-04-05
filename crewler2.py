#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 06:38:38 2018

@author: FongWunChen
"""

import requests
from bs4 import BeautifulSoup


r = requests.get('https://book.douban.com/subject/1084336/comments/')
soup = BeautifulSoup(r.text, 'lxml') 
pattern = soup.find_all('p', 'comment-content')
listA = []
sum = 0
for item in pattern:
    listA.append(item.string) 

for name in listA:
    print(name)
    print(len(name))
    sum = sum + len(name)
    print('------')
          
print(sum)         
           