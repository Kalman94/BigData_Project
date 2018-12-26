from __future__ import division
from xxhash import xxh32
import numpy as np
from collections import Counter
import json
DTYPE = np.int64
 
 #Define Count Min sketch class
class CountMinSketch(object):
 
    def __init__(self, _w=None, _d=None, _delta=None, _epsilon=None):
        """
        CountMinSketch is an implementation of the count min sketch
        algorithm that probabilistically counts string frequencies.
 
        You must either supply w and d directly, or let them be calculated form error,
        delta, and epsilon. If You choose the latter, then w = ceil(error/epsilon) and
        d = ceil(ln(1.0/delta)) where the error in answering a query is within a factor
        of epsilon with probability delta.
 
        Parameters
        ----------
        w : the number of columns in the count matrix
        d : the number of rows in the count matrix
        delta : (not applicable if w and d are supplied) the probability of query error
        epsilon : (not applicable if w and d are supplied) the query error factor
 
        bits : The size of the hash output space
 
        For the full paper on the algorithm, see the paper
        "An improved data stream summary: the count-min sketch and its -
        applications" by Cormode and Muthukrishnan, 2003.
        """
 
        if _w is not None and _d is not None:
            self.w = _w
            self.d = _d
        elif _delta is not None and _epsilon is not None:
            self.w = np.ceil(np.e / _epsilon)
            self.d = np.ceil(np.log(1./_delta))
        else:
            raise Exception(
                "You must either supply both w and d or delta and epsilon.")
 
        self.count = np.zeros((self.d, self.w), dtype=DTYPE)
        self.rows = np.arange(self.d)
        self.shift_by = np.ceil(np.log(self.w) / np.log(2))
 
    def get_columns(self, a):
        a_string = str(a)
        hashes = np.zeros(self.d, dtype=DTYPE)
        h = xxh32(a_string).intdigest()
 
        for i in range(self.d):
            hashes[i] = h % self.w
            h >= self.shift_by
            if h < self.w and i < self.d:
                cur_string = str(i) + a_string
                h = xxh32(cur_string).intdigest()
 
        return hashes
 
    def update(self, a, val=1):
        h = self.get_columns(a)
        self.count[self.rows, h] += val
 
    def query(self, a):
        h = self.get_columns(a)
        return self.count[self.rows, h].min()
 
    def __getitem__(self, a):
        return self.query(a)
 
    def __setitem__(self, a, val):
        cur = self.query(a)
        self.update(a, val - cur)
        
cms = CountMinSketch(272, 7)
tweets = []
for line in open('C:\\Users\\teo\\Desktop\\tweets.json.0', 'r',encoding="utf-8"):
    tweets.append(json.loads(line))


hashtags = []
for i in tweets:
    if 'entities' in i:
        hashtags.extend(i['entities']['hashtags'])
hashtags = [tag['text'] for tag in hashtags]  
for tag in hashtags:
    cms.update(tag)
 # With the help of counter and most common function we can get in dict the tags paired with their counter
a=Counter(hashtags).most_common()[:10]

#get the counter for the tags below from count min with the __getitem__method
print(cms.__getitem__('Crimea'))
print(cms.__getitem__('Ukraine'))
print(cms.__getitem__('Russia'))
print(cms.__getitem__('usa'))
print(cms.__getitem__('Putin'))
print(cms.__getitem__('ipad'))
print(cms.__getitem__('anal'))
print(cms.__getitem__('milf'))
print(cms.__getitem__('xxx'))
print(cms.__getitem__('USA'))
