# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 16:25:59 2017

@author: teo
"""
import hyperloglog
 
# accept 1% counting error in our approach
hll = hyperloglog.HyperLogLog(0.01)


from collections import Counter
from array import array
from random import randint
from math import log, e, ceil
from itertools import zip_longest
import hashlib
import array


#Load tweets from json file to a list
tweets=[]
for line in open('C:\\Users\\teo\\Desktop\\tweets.json.0', 'r',encoding="utf8"):
    tweets.append(json.loads(line))

# Create a list where we are going to save our hashtags
hashtags = []
for i in tweets:
    if 'entities' in i:
        hashtags.extend(i['entities']['hashtags'])#as we loop through json we pick up every word inside entities{hashtags:}
        
        
        
#We are looking for only hashtags with text and no empty     
hashtags = [tag['text'] for tag in hashtags]  


# save all the hashtags inside hyperloglog function
for tag in hashtags:
     hll.add(tag)
#by printing the length of the hyperloglog list we can find the distinct elements
print (len(hll))    


# We are using set to remove dublicates and then the  len function to count the elements in the set
print (len(set(hashtags)))