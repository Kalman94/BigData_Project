# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 17:19:47 2017

@author: teo
"""
import sys
#import libraries
import operator
from operator import itemgetter
import json
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from array import array
from random import randint
from math import log, e, ceil
from itertools import zip_longest
import hashlib
import array
import itertools
import numpy as np
tweets=[]
for line in open('C:\\Users\\teo\\Desktop\\tweets.json.0', 'r',encoding="utf8"):
    tweets.append(json.loads(line))


hashtags = []
for i in tweets:
    if 'entities' in i:
        hashtags.extend(i['entities']['hashtags'])
        
     
        
        
hashtags = [tag['text'] for tag in hashtags]  
 
        
# using bult in counter we count the most common hashtags and save into a dictionary, every hashtag paired with its frequency
D=dict(Counter(hashtags).most_common(6))
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())

plt.show()


TagsDict=dict(Counter(hashtags).most_common())
df = pd.DataFrame(TagsDict,index=[0]).T  # transpose to look just like the sheet above
df.to_csv('tag-counter.csv')
