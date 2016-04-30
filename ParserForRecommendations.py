'''
Python program used to parse a particular review
'''

import urllib, urllib2, time
import StringIO
from xml.dom.minidom import parse
import sys
import os
import json

# takes input file path 
inputFilePath = sys.argv[1]

# opens the input file
inputFile = open(inputFilePath, 'rU')
# reads input file
the_page = inputFile.read()
#close input file
inputFile.close()

# extracting directory name of the input file
directory = os.path.dirname(inputFilePath)

#extracting the file Name fron the path
inputFileName = os.path.basename(inputFilePath)

#opening output File
ouputFile = open(directory + "\\" + inputFileName + "parsed_for_recommend.txt", 'w')

#creating the output dictionary
dict = {}


#method to form Dictionary 
def formDictionary(key, value):
    # check if the key is present in the dictionary or not 
    if (dict.has_key(key)):
        dict[key].append(value);
    else:
        dict[key] = [value]

#print the_page
dom = parse(StringIO.StringIO(the_page))
# extracting the all item tags from the given XML
name = dom.getElementsByTagName('item')

#iterating over each item
for child in name:
    #get the title attribute from the item
    title = child.getElementsByTagName('title')[0]
    
    #get the reviewer attribute from the item
    user = child.getElementsByTagName('reviewer')[0]
    
    #get the rating attribute from the item
    rating = child.getElementsByTagName('rating')[0]

    #condition to check if the corresponding tag is present in the item
    if (title.hasChildNodes is not None and len(title.childNodes) > 0 and title.childNodes[0].data is not None
        and user.hasChildNodes is not None and len(user.childNodes) > 0 and user.childNodes[0].data is not None
        and rating.hasChildNodes is not None and len(rating.childNodes) > 0 and rating.childNodes[0].data is not None):
       
        key = user.childNodes[0].data
        value = (title.childNodes[0].data, rating.childNodes[0].data)
       
        #adding the tag in the dictionary
        formDictionary(key, value)

#writing output in the dictionary
for key in sorted(dict):
    for (title, rating) in dict[key]:
        ouputFile.write(key.encode("utf-8") + "\t" +  rating.encode("utf-8")   + "\t" +title.encode("utf-8"))
        ouputFile.write("\n")
