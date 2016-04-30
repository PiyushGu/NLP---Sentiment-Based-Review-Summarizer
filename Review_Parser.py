'''
This python program is used for parsing the books, dvd and music xml file and storing that in the file using \
JSON format
'''
import StringIO
from xml.dom.minidom import parse
import sys
import os
import json
import langdetect


#method to build review dictionary 
def build_dictionary(review_page):
    #dictionary for each product
    product = {}
    #counter used to detect review for particular product
    counter = 0
    #parsing the review page
    dom = parse(StringIO.StringIO(review_page))
    
    #extracting the item tags
    name = dom.getElementsByTagName('item')
    #iterating over each item
    for child in name:
        #extracting the given title tag from the item
        title = child.getElementsByTagName('title')[0]
        #extracting the text title from the item
        text = child.getElementsByTagName('text')[0]

        #checking if the corresponding tag is present in the item
        if(title.hasChildNodes is not None and len(title.childNodes) > 0 and  title.childNodes[0].data is not None
            and text.hasChildNodes is not None and len(text.childNodes) > 0 and  text.childNodes[0].data is not None):
            key = title.childNodes[0].data
            value = text.childNodes[0].data

            #checking if the product is present in the dictionary
            if key in product:
                product[key].append(value)
            else:
                #if the product is not present, then adding that in the dictionary, based on the language
                if counter == 0:
                    #langdect library used to detect the language of the particular review
                    language = langdetect.detect(value)
                    counter += 1
                product[key] = [value]
    dictionary = (language, product)
    return dictionary

if __name__ == '__main__':
    #reading the input file path 
    inputDirectory = sys.argv[1]
    #book reviews dictionary
    books_reviews_list = []

    #dvd reviews dictionary
    dvd_reviews_list = []
    
    #music  reviews dictionary
    music_reviews_list = []

    #walking over the the input directory to find the review files
    for root, dirs, files in os.walk(inputDirectory):
        for each_file in files:
           #the review file are in text document
            if each_file.endswith('txt'):
                fileName = os.path.join(root, each_file)
                inputFile = open(fileName, 'r')
                the_page = inputFile.read()
                inputFile.close()

                #the book review file name are starting with books
                if each_file.startswith('books'):
                    #forming the dictiorary of review from the given input
                    books_reviews = build_dictionary(the_page)
                    #print("Parsed XML for books_reviews in " + books_reviews[0])
                    books_reviews_list.append(books_reviews)

                #the dvd review file name are starting with dvd
                elif each_file.startswith('dvd'):
                    #forming the dictiorary of review from the given input
                    dvd_reviews = build_dictionary(the_page)
                    #print("Parsed XML for DVD_reviews in " + dvd_reviews[0])
                    dvd_reviews_list.append(dvd_reviews)

                #the music review file name are starting with books
                elif each_file.startswith('music'):
                    #forming the dictiorary of review from the given input
                    music_reviews = build_dictionary(the_page)
                    #print("Parsed XML for Music_reviews in " + music_reviews[0])
                    music_reviews_list.append(music_reviews)

    #buiding dictionary of dictionary and dumping it into the file 
    dictionaries = [books_reviews_list, dvd_reviews_list, music_reviews_list]
    jsonData = json.dumps(dictionaries)
    outFile = open("XML_Parsed_Dictionary.txt",'w')
    outFile.write(jsonData)
    outFile.close()
