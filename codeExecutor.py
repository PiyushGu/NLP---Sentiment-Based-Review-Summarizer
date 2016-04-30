import os
import sys


os.system('python Review_Parser.py ' + sys.argv[1])
os.system('python Tagging_Shallow_Parsing.py XML_Parsed_Dictionary.txt')
os.system('python Sentiment_Syntactic_Analyser.py Summarized_Review_List.txt')
