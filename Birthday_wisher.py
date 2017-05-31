#!/usr/bin/python

# intial code for freinds birtday wisher 
import time

bday_list = {}

infile = open("DOB_Name_List.txt")
for line in infile:
    List_array = [w.strip() for w in line.split("\t")]
    bday_list[List_array[0]] = List_array[1]
    print line

# To check dictionary created properly
print bday_list


for key in bday_list:
    print "DOB in MM/DD : " + key + "\t" + "Name " + bday_list[key]

#    print time.strftime("%x")[:5] + key
#    print "key: " + key + "\t" + "value " + bday_list[key]


# To check present date with list in dictionary if matches send msg to wish

if time.strftime("%x")[:5] == key : 
    print 'happy birthday ' + bday_list[key]
else:
    print 'nope'

