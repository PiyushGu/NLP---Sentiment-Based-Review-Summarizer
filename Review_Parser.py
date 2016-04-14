import StringIO
from xml.dom.minidom import parse
import sys
import os
import json
import langdetect




def build_dictionary(review_page):
    product = {}
    counter = 0
    dom = parse(StringIO.StringIO(review_page))
    name = dom.getElementsByTagName('item')
    for child in name:
        title = child.getElementsByTagName('title')[0]
        text = child.getElementsByTagName('text')[0]
        if(title.hasChildNodes is not None and len(title.childNodes) > 0 and  title.childNodes[0].data is not None
            and text.hasChildNodes is not None and len(text.childNodes) > 0 and  text.childNodes[0].data is not None):
            key = title.childNodes[0].data
            value = text.childNodes[0].data
            if key in product:
                product[key].append(value)
            else:
                if counter == 0:
                    language = langdetect.detect(value)
                    counter += 1
                product[key] = [value]
    dictionary = (language, product)
    return dictionary

if __name__ == '__main__':
    inputDirectory = sys.argv[1]
    books_reviews_list = []
    dvd_reviews_list = []
    music_reviews_list = []
    for root, dirs, files in os.walk(inputDirectory):
        for each_file in files:
            if each_file.endswith('txt'):
                fileName = os.path.join(root, each_file)
                inputFile = open(fileName, 'r')
                the_page = inputFile.read()
                inputFile.close()
                if each_file.startswith('books'):
                    books_reviews = build_dictionary(the_page)
                    books_reviews_list.append(books_reviews)
                elif each_file.startswith('dvd'):
                    dvd_reviews = build_dictionary(the_page)
                    dvd_reviews_list.append(dvd_reviews)
                elif each_file.startswith('music'):
                    music_reviews = build_dictionary(the_page)
                    music_reviews_list.append(music_reviews)
    for each in books_reviews_list:
        print(each[0])
    for each in dvd_reviews_list:
        print(each[0])
    for each in music_reviews_list:
        print(each[0])
    dictionaries = [books_reviews_list, dvd_reviews_list, music_reviews_list]
    jsonData = json.dumps(dictionaries)
    outFile = open("parsed_dictionaries",'w')
    outFile.write(jsonData)
    outFile.close()
