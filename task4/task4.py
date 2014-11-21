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
import collections

#timespan in seconds (whole day:86400)
timespan = 86400
#scale of the graph (size of the time slots) in seconds
skalierung = 60
#only show topics in the plot that have at least x tweets
thresh = 12000
maxPlot = 20

def getHashtags(row):
     return re.findall(r"#(\w+)", row)

#had to use this method because one entry had an 'r' in it        
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False        

print 'Start reading csv-file...'
file = open('../data/numeric_20140712.csv', "rU")
a = csv.reader(file,delimiter='\t')

geoValue = {}

print 'Start computing and counting topics...'
for row in a:
    #only take rows with all columns
    if(len(row) > 5):
        latidute = row[3]
        longitude = row[4]
        date = row[2]
        #only take geolocations that can be passed        
        if(is_number(longitude) and is_number(latidute) and is_number(date)):
               
                #random rounding
                geoLoc=(round(float(latidute)),round(float(longitude)))
                
                #just ignoring the 0,0 guys
                if geoLoc != (0,0):
                    hour = long(date[8:10])
                    minute = long(date[10:12])
                    second = long(date[12:14])
                    index = (hour * 3600 + minute * 60 + second) / skalierung
                    if index >= timespan/skalierung:
                        break

                    try:
                        geoValue[index]
                    except KeyError:
                        geoValue[index] = {}
                    
                    try:
                        geoValue[index][geoLoc] += 1
                    except LookupError:
                        geoValue[index][geoLoc] = 1

                  
file.close()

json = open('loc.json','w')
json.write('[')

for i in range(1440):
    json.write('[\n'+str(i)+',[ ')
    series = ''
    for loc in geoValue[i].items():
        ((lat,lon),mag) = loc
        series = series + str(lat)+','+str(lon)+','+str(mag)+','
    #delete last comma
    series.rstrip(',')
    json.write(series)
    json.write(']\n]')
    #beautiful code!! have to get rid of last comma ;)    
    if i < 1439:
        json.write(',')

json.write('];')
json.close()


    
