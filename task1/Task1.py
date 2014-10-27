# -*- coding: utf-8 -*-
"""
This class should solve the first Task for Social Data Mining.

Created on Mon Oct 20 23:25:58 2014

@author: Henning Wübben, Lukas Rein, Andrea Suckro
"""
import csv
#import pylab as plt
import matplotlib.pyplot as plt
import numpy as np
import re
import math
#timespan in seconds (whole day:86400)
timespan = 86400
#scale of the graph (size of the time slots) in seconds
scale = 60.0
#search pattern (regex), for all tweets just put ""
#pattern = "g+o+a+l+|t+o+r+|m+e+t+a+|g+o+l+"
pattern = ""

def contains(row, pattern):
    if(re.search(pattern, row)):
        return True
    else:
        return False 
        
#had to use this method because one entry had an 'r' in it        
def is_number(s):
    try:
        long(s)
        return True
    except ValueError:
        return False

#READING THE FILE
file_1207 = open('../data/numeric_20140712.csv', "rU")
a = csv.reader(file_1207,delimiter='\t')

file_1307 = open('../data/numeric_20140713.csv', "rU")
b = csv.reader(file_1307,delimiter='\t')

file_1407 = open('../data/numeric_20140714.csv', "rU")
c = csv.reader(file_1407,delimiter='\t')

#PROCESSING OF THE DATA
num_points = math.ceil(timespan/scale)
timesA = np.zeros(num_points)
timesB = np.zeros(num_points)
timesC = np.zeros(num_points)
xVal = np.arange(num_points) 

for row in a:
    if(len(row) > 5):
        date = row[2]            
        if(is_number(date)):
            if(contains(row[6].lower(),pattern.lower())):
                hour = long(date[8:10])
                minute = long(date[10:12])
                second = long(date[12:14])
                index = hour * 3600 + minute * 60 + second
                if(index >= timespan):
                    break
                timesA[index/scale] += 1  

            
file_1207.close()

for row in b:
    if(len(row) > 5):
        date = row[2]            
        if(is_number(date)):
            if(contains(row[6].lower(),pattern.lower())):
                hour = long(date[8:10])
                minute = long(date[10:12])
                second = long(date[12:14])
                index = hour * 3600 + minute * 60 + second
                if(index >= timespan):
                    break
                timesB[index/scale] += 1  

            
file_1307.close()

for row in c:
    if(len(row) > 5):
        date = row[2]            
        if(is_number(date)):
            if(contains(row[6].lower(),pattern.lower())):
                date = row[2]
                hour = long(date[8:10])
                minute = long(date[10:12])
                second = long(date[12:14])
                index = hour * 3600 + minute * 60 + second
                if(index >= timespan):
                    break
                timesC[index/scale] += 1  

           
file_1407.close()


fig = plt.figure()
fig.suptitle('All tweets', fontsize=14, fontweight='bold')

#plot for 12.07
ax = fig.add_subplot(221)
fig.subplots_adjust(top=0.85)
ax.set_title('12.07.2014')
ax.set_xlabel('Time in minutes')
ax.set_ylabel('Number of Tweets')
ax.plot(xVal,timesA)

bx = fig.add_subplot(222)
fig.subplots_adjust(top=0.85)
bx.set_title('13.07.2014')
bx.set_xlabel('Time in minutes')
bx.set_ylabel('Number of Tweets')
bx.plot(xVal,timesB)

cx = fig.add_subplot(223)
fig.subplots_adjust(top=0.85)
cx.set_title('14.07.2014')
cx.set_xlabel('Time in minutes')
cx.set_ylabel('Number of Tweets')
cx.plot(xVal,timesC)

plt.show()