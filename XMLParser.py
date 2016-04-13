import urllib, urllib2, time
import StringIO
from xml.dom.minidom import parse
import sys
import os
import json


inputFilePath = sys.argv[1]
inputFile = open(inputFilePath)
the_page = inputFile.read()
inputFile.close()

directory = os.path.dirname(inputFilePath)
print directory
inputFileName = os.path.basename(inputFilePath)


ouputFile = open(directory + "\\" + inputFileName + "_parsed.txt" ,'w')

dict = {}
def WriteTagInFile(tag,tagName):

     if(tag.hasChildNodes is not None and len(tag.childNodes) > 0 and  tag.childNodes[0].data is not None):
        ouputFile.write(tagName)
        ouputFile.write("\n")
        ouputFile.write((tag.childNodes[0].data).encode("utf-8"))
        ouputFile.write("\n")

def formDictiorany(title,review):

     if(dict.has_key(title)):
           dict[title].append(review);
     else:
           dict[title] = [review]

#print the_page 
dom = parse(StringIO.StringIO(the_page))
name = dom.getElementsByTagName('item')
#name[0].firstChild
for child in name:
    title = child.getElementsByTagName('title')[0]
    text = child.getElementsByTagName('text')[0]

    if(title.hasChildNodes is not None and len(title.childNodes) > 0 and  title.childNodes[0].data is not None
        and text.hasChildNodes is not None and len(text.childNodes) > 0 and  text.childNodes[0].data is not None):
        key  = title.childNodes[0].data
        value = text.childNodes[0].data
        
        formDictiorany(key,value)

for key in dict:
    ouputFile.write(key.encode("utf-8"))
    ouputFile.write("\n")
    ouputFile.write(str(dict[key]))
    ouputFile.write("\n")
    ouputFile.write("\n")
