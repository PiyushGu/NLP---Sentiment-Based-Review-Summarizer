import urllib, urllib2, time
import StringIO
from xml.dom.minidom import parse
import sys
import os
import json


inputFilePath = sys.argv[1]

# inputFilePath = r"C:\Users\Piyush\Desktop\NLP Project\Corpus\cls-acl10-unprocessed\fr\dvd\testFile.review"
inputFile = open(inputFilePath, 'rU')
the_page = inputFile.read()
inputFile.close()

directory = os.path.dirname(inputFilePath)
print directory
inputFileName = os.path.basename(inputFilePath)

ouputFile = open(directory + "\\" + inputFileName + "parsed_for_recommend.txt", 'w')

dict = {}


def formDictiorany(key, value):
    if (dict.has_key(key)):
        dict[key].append(value);
    else:
        dict[key] = [value]

#print the_page
dom = parse(StringIO.StringIO(the_page))
name = dom.getElementsByTagName('item')
#name[0].firstChild
for child in name:
    title = child.getElementsByTagName('title')[0]
    user = child.getElementsByTagName('reviewer')[0]
    rating = child.getElementsByTagName('rating')[0]

    if (title.hasChildNodes is not None and len(title.childNodes) > 0 and title.childNodes[0].data is not None
        and user.hasChildNodes is not None and len(user.childNodes) > 0 and user.childNodes[0].data is not None
        and rating.hasChildNodes is not None and len(rating.childNodes) > 0 and rating.childNodes[0].data is not None):
        key = user.childNodes[0].data
        value = (title.childNodes[0].data, rating.childNodes[0].data)

        formDictiorany(key, value)

for key in sorted(dict):
    for (title, rating) in dict[key]:
        ouputFile.write(key.encode("utf-8") + "\t" +  rating.encode("utf-8")   + "\t" +title.encode("utf-8"))
        ouputFile.write("\n")
