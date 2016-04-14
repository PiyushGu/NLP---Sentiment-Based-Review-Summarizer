import StringIO
import pattern.fr
import pattern.de
from xml.dom.minidom import parse
import sys
import os
import json
from textblob_de import TextBlobDE as TextBlob


def getFeatureDict(review_Dict, lang):
    feature_dict = {}
    print(lang)
    for keys in review_Dict:
        features_list = [] # list of identified feature,descriptor pair
        for review in review_Dict[keys]: # for each review for a title
            # print(pattern.fr.tag(review))
            review_list = review.split(".")
            # for each line in a review
            for each_review in review_list:
                if lang == 'fr':
                    tagged_review = pattern.fr.tag(each_review, tokenize=True)
                elif lang == 'de':
                    tagged_review = pattern.de.tag(each_review, tokenize=True)
                else:
                    tagged_review = " "
                print(tagged_review)
                features_present = False
                for i in range(0, len(tagged_review)):
                    # check for the possible tag combinations

                    if tagged_review[i][1] == "JJ": # check for tag JJ
                        features_present = True
                        feature = None
                        descriptor = tagged_review[i][0]
                        if i+1 < len(tagged_review):
                            if tagged_review[i+1][1] == "NN" or tagged_review[i+1][1] == "NNS":
                                feature = tagged_review[i+1][0]
                        if i-1 >= 0 and feature is None:
                            if tagged_review[i-1][1] == "NN" or tagged_review[i-1][1] == "NNS":
                                feature = tagged_review[i-1][0]
                        if feature is None:
                            feature_back = None
                            feature_front = None
                            j = i+1
                            k = i-1
                            while j < len(tagged_review):
                                if tagged_review[j][1] == "NN" or tagged_review[j][1] == "NNS":
                                    feature_back = tagged_review[j][0]
                                    break
                                j += 1
                            while k >= 0:
                                if tagged_review[k][1] == "NN" or tagged_review[k][1] == "NNS":
                                    feature_front = tagged_review[k][0]
                                    break
                                k -= 1
                            if (j-i) < (i-k) and feature_back is not None:
                                feature = feature_back
                            elif feature_front is not None:
                                feature = feature_front
                        features_list.append((descriptor, feature))

                    if tagged_review[i][1] == "RB":
                        if i+1 < len(tagged_review):
                            if tagged_review[i+1][1] == "VBN":
                                features_present = True
                                descriptor = tagged_review[i][0]
                                feature = tagged_review[i+1][0]
                                features_list.append((descriptor, feature))

                    if tagged_review[i][1] == "RB":
                        if i+1 < len(tagged_review):
                            if tagged_review[i+1][1] == "NN" or tagged_review[i+1][1] == "NNS":
                                features_present = True
                                descriptor = tagged_review[i][0]
                                feature = tagged_review[i+1][0]
                                features_list.append((descriptor, feature))


                #append sentiment for the line which has features present
                if features_present:
                    if lang == 'fr':
                        features_list.append(pattern.fr.sentiment(each_review))
                    elif lang == 'de':
                        features_list.append(TextBlob(each_review).sentiment)

        # display all the feature pairs along with the sentiments
        for each_pair in features_list:
            if type(each_pair[0]) == unicode:
                if each_pair[0] is not None and each_pair[1] is not None:
                    print(each_pair[0].encode('utf-8') +" "+ each_pair[1].encode('utf-8'))
            else:
                print(each_pair)
        print
        # print(pattern.fr.sentiment(review_Dict[keys][0]))
        # print(pattern.fr.tag(review_Dict[keys][0], tokenize=True))
        # print
        # s = pattern.fr.parsetree(review_Dict[keys][0],relations=True, lemmata=True)
        # for sentence in s:
        #     for chunk in sentence.chunks:
        #         for word in chunk.words:
        #             print word,
        #         print
        #     print


def parseInput():
    inputFile = open(sys.argv[1])
    books_reviews_list, dvd_reviews_list, music_reviews_list = json.load(inputFile)

    for each in books_reviews_list:
        getFeatureDict(each[1], each[0])

    # for each in dvd_reviews_list:
    #     getFeatureDict(each[1], each[0])
    #
    # for each in music_reviews_list:
    #     getFeatureDict(each[1], each[0])

    inputFile.close()



if __name__ == '__main__':
    parseInput()





