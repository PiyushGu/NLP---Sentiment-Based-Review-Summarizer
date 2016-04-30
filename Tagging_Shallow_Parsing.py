import pattern.fr
import pattern.de
import sys
import json
import codecs


def dependency_parser(review):
    s = pattern.fr.parse(review).split()


def getFeatureDict(review_Dict, lang):
    summarized_dict = {}
    for keys in review_Dict:
        feature_list = []
        for review in review_Dict[keys]: # for each review for a title
            dependency_parser(review)
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
                for i in range(0, len(tagged_review)):
                    features_present = False
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
                            if feature_front is None and feature_back is not None:
                                feature = feature_back
                            elif feature_back is None and feature_front is not None:
                                feature_back = feature_front
                            elif (j-i) < (i-k):
                                feature = feature_back
                            else:
                                feature = feature_front

                    if tagged_review[i][1] == "RB":
                        if i+1 < len(tagged_review):
                            if tagged_review[i+1][1] == "NN" or tagged_review[i+1][1] == "NNS":
                                features_present = True
                                descriptor = tagged_review[i][0]
                                feature = tagged_review[i+1][0]

                    if tagged_review[i][1] == "NN":
                        if i+1 < len(tagged_review):
                            if tagged_review[i+1][1] == "NN" or tagged_review[i+1][1] == "NNS":
                                features_present = True
                                descriptor = tagged_review[i][0]
                                feature = tagged_review[i+1][0]

                    # append the descriptor feature pair onl if the sentiment is not 0
                    if features_present:
                        if descriptor != None and feature != None:
                            feature_list.append((descriptor, feature))
        summarized_dict[keys] = feature_list
    return summarized_dict



def parseInput():
    inputFile = open(sys.argv[1])
    books_reviews_list, dvd_reviews_list, music_reviews_list = json.load(inputFile)
    books_summary = []
    dvd_summary = []
    music_summary = []

    for each in books_reviews_list:
        summary = getFeatureDict(each[1], each[0])
        books_summary.append((each[0], summary))

    for each in dvd_reviews_list:
        summary = getFeatureDict(each[1], each[0])
        dvd_summary.append((each[0], summary))

    for each in music_reviews_list:
        summary = getFeatureDict(each[1], each[0])
        music_summary.append((each[0], summary))
    inputFile.close()

    summaries = [books_summary, dvd_summary, music_summary]
    jsonData = json.dumps(summaries)
    outFile = open("Summarized_Review_List.txt",'w')
    outFile.write(jsonData)
    outFile.close()


if __name__ == '__main__':
    parseInput()





