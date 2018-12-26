# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 09:14:20 2017

@author: teo
"""


import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from array import array
from random import randint
from math import log, e, ceil
from itertools import zip_longest

from pandas import DataFrame


from collections import Counter


tweets = []
for line in open('C:\\Users\\teo\\Desktop\\tweets.json.0', 'r', encoding='utf-8'):
    tweets.append(json.loads(line))


tweet = tweets[0]

#store in specific lists the information inside the tweets
ids = [tweet['id_str'] for tweet in tweets if 'id_str' in tweet] 
names= [tweet['user']['name'] for tweet in tweets if 'user' in tweet]                    
User_id= [tweet['user']['id'] for tweet in tweets if 'user' in tweet]
hashtags=[tweet['entities']['hashtags'] for tweet in tweets if 'entities' in tweet]     
text = [tweet['text'] for tweet in tweets if 'text' in tweet]
lang = [tweet['lang'] for tweet in tweets if 'lang' in tweet]
geo = [tweet['geo'] for tweet in tweets if 'geo' in tweet]                    
place = [tweet['place'] for tweet in tweets if 'place' in tweet]

#create dataframe for the reala data
df=pd.DataFrame({'Ids':pd.Index(ids),
                 'Names':pd.Index(names),
                 'User_Id':pd.Index(User_id),
                 'Hashtags':pd.Index(hashtags),
                 'Text':pd.Index(text),
                 'Lang':pd.Index(lang),
                 'Geo':pd.Index(geo),
                 'Place':pd.Index(place)})

# Create a groupby object in order to group by our df based on posts

df.groupby('Text').count()
#produce a sub dataframe which containes users and the number of their posts
c=df.User_Id.value_counts()




#Sorted_2 = df.sort_values(['Hashtags'], ascending=False)


#create a small function needed inside sampling function to help us produce a list of zeros
def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros
#the priority sampling function 
def prioritySampling (stream, sampleSize):
    """Sampling method 3: Priority Sampling with sampling window
        'stream' is the stream to sample from
        'sampleSize'is the size of the sample
    """
    
    sample=np.zeros((sampleSize),dtype=object)
    tags=np.zeros(sampleSize)
    samples=zerolistmaker(sampleSize)
    
    i=0
    j=0
    while i<len(stream):
        if i<sampleSize:
            sample[i] = stream[i]
            samples[i] = stream[i]
            tags[i] = np.random.random()
        else:
            newTag = np.random.random()
            maxTag = np.max(tags)
            idxMaxTag = np.argmax(tags)
            
            if maxTag > newTag:
                sample[idxMaxTag]=stream[i]
                samples[idxMaxTag] = stream[i]
                tags[idxMaxTag]=newTag
                j=j+1
        i=i+1
    print ('updates priority=',j)    
    return samples
	# reservoir sample function nothing changed from the original in lab
def reservoir_sample(stream, size):
    """
    maintains a random sample from a stream.
    Args:
        stream: iterable item
        size: size of the sample you want
    """
    reservoir = []    
    for i, x in enumerate(stream, start=1):
        if i <= size:
            reservoir.append(x)
        elif random.random() < (1 / i):
            reservoir[random.randint(0, size-1)] = x
    return reservoir   



#call the functions  from the original stream and pick up 100 samples for each sampling method
reserve_sample=reservoir_sample(tweets,100)  
priority_sample=prioritySampling(tweets,100)        


#create lists for samplings and fill them with the tweets that have been collected
reservoir_list=[]
priority_list=[]


for line in reserve_sample:
   reservoir_list.append(line)
   
for line in priority_sample:
   priority_list.append(line)
reservoir_sample_tweet=reservoir_list[0]
priority_sample_tweet=priority_list[0]

r_ids = [reservoir_sample_tweet['id_str'] for reservoir_sample_tweet in reservoir_list if 'id_str' in reservoir_sample_tweet] 
r_names= [reservoir_sample_tweet['user']['name'] for reservoir_sample_tweet in reservoir_list if 'user' in reservoir_sample_tweet]                    
r_User_id= [reservoir_sample_tweet['user']['id'] for reservoir_sample_tweet in reservoir_list if 'user' in reservoir_sample_tweet]
r_hashtags=[reservoir_sample_tweet['entities']['hashtags'] for reservoir_sample_tweet in reservoir_list if 'entities' in reservoir_sample_tweet]     
r_text = [reservoir_sample_tweet['text'] for reservoir_sample_tweet in reservoir_list if 'text' in reservoir_sample_tweet]

p_ids = [priority_sample_tweet['id_str'] for priority_sample_tweet in priority_list if 'id_str' in priority_sample_tweet] 
p_names= [priority_sample_tweet['user']['name'] for priority_sample_tweet in priority_list if 'user' in priority_sample_tweet]                    
p_User_id= [priority_sample_tweet['user']['id'] for priority_sample_tweet in priority_list if 'user' in priority_sample_tweet]
p_hashtags=[priority_sample_tweet['entities']['hashtags'] for priority_sample_tweet in priority_list if 'entities' in priority_sample_tweet]     
p_text = [priority_sample_tweet['text'] for priority_sample_tweet in priority_list if 'text' in priority_sample_tweet]



df_reservoir=pd.DataFrame({'Ids':pd.Index(r_ids),
                 'Names':pd.Index(r_names),
                 'User_Id':pd.Index(r_User_id),
                 'Hashtags':pd.Index(r_hashtags),
                 'Text':pd.Index(r_text)})
df_priority=pd.DataFrame({'Ids':pd.Index(p_ids),
                 'Names':pd.Index(p_names),
                 'User_Id':pd.Index(p_User_id),
                 'Hashtags':pd.Index(p_hashtags),
                 'Text':pd.Index(p_text)})
    
    
# After looping through sampling lists we create one dataframe for each sampling method to make our life easier as the first one with real data
 
# Same idea as first df with real data using groupby and userid.value_counts() to find all the users active and least in a dataframe
#this time users will be saved in c_res and c_pr for each sampling method

 
df_reservoir.groupby('Text').count()


c_res=df_reservoir.User_Id.value_counts()
df_priority.groupby('Text').count()


c_pr=df_priority.User_Id.value_counts()
hashtags_pp=[]
hashtags_rr=[]
hashtags_p=[]
for i in priority_list:
    if 'entities' in i:
        hashtags_p.extend(i['entities']['hashtags'])
hashtags_r = []
for i in reservoir_list:
    if 'entities' in i:
        hashtags_r.extend(i['entities']['hashtags'])
        
hashtags_pp = [tag['text'] for tag in hashtags_p]  
hashtags_rr = [tag['text'] for tag in hashtags_r]  

#for hashtags we can loop through them and vissualize them as the Q1 question,we use second list for each sampling method
#because we want the words inside texts and not the whole hashtag json schema as saved in dataframe
                 
D_p=dict(Counter(hashtags_pp).most_common(6))
plt.bar(range(len(D_p)), D_p.values(), align='center')
plt.xticks(range(len(D_p)), D_p.keys())

plt.show()
D_r=dict(Counter(hashtags_rr).most_common(6))
plt.bar(range(len(D_r)), D_r.values(), align='center')
plt.xticks(range(len(D_r)), D_r.keys())

plt.show()
