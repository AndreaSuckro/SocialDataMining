# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 19:25:58 2014

@author: Henning Wübben, Lukas Rein, Andrea Suckro
"""
import csv
import pylab as plt
import numpy as np
import re
import operator
#timespan in seconds (whole day:86400)
timespan = 86400
#scale of the graph (size of the time slots) in seconds
skalierung = 60
#only show topics in the plot that have at least x tweets
thresh = 500

def getHashtags(row):
     return re.findall(r"#(\w+)", row)

#had to use this method because one entry had an 'r' in it        
def is_number(s):
    try:
        long(s)
        return True
    except ValueError:
        return False        

print 'Start reading csv-file...'
file = open('../data/numeric_20140713.csv', "rU")
a = csv.reader(file,delimiter='\t')

regEx = np.array(np.zeros(timespan/skalierung), dtype = dict)

for i in range(len(regEx)):
    regEx[i] = {}

print 'Start computing and counting topics...'
for row in a:
    if(len(row) > 5):
        
        value = row[2]
        if is_number(value): 
            hour = long(value[8:10])
            minute = long(value[10:12])
            second = long(value[12:14])
            index = (hour * 3600 + minute * 60 + second) / skalierung
            if index >= timespan/skalierung:
                break
        
            matches = getHashtags(row[6])
        
            for match in matches:
                matchL = match.lower()
                try:
                    regEx[index][matchL] += 1
                except LookupError:
                    regEx[index][matchL] = 1
                  
file.close()

toPlot = {}

print 'Plot data...'

fig = plt.figure()
fig.suptitle('Hot Topics!')
plt.xlabel('Time in minutes')
plt.ylabel('Number of tweets in topic')

for index,dic in enumerate(regEx):
    if len(dic) >= 5:
        biggest = dict(sorted(dic.iteritems(), key=operator.itemgetter(1),
                              reverse=True)[:5])
    else:
        biggest = dict(sorted(dic.iteritems(), key=operator.itemgetter(1),
                              reverse=True)[:len(dic)])                 
    for hashtag in biggest:
        try:
            toPlot[hashtag][index] = biggest[hashtag]
        except LookupError:
            toPlot[hashtag] = np.zeros(timespan / skalierung)
            toPlot[hashtag][index] = biggest[hashtag]
labels = []
curves = []
for hashtag in toPlot:
    if max(toPlot[hashtag]) > thresh:
        line, = plt.plot(toPlot[hashtag], label = hashtag)
        labels.append(hashtag)
        curves.append(line)
plt.legend(curves,labels,loc="upper left")
#plt.legend(labels)

plt.show()
        


