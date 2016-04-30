'''
Python program which is used to find Sentiment and Semantic similarity of the given sentence of French and German
'''

import sys, json
import pattern.fr
from textblob_de import TextBlobDE as TextBlob
import subprocess
import os
from multiprocessing import pool

#method to find the sentiment of given summary based on the given language
def sentiment_analyser(summary, lang):
    #dictionary to  final features
    final_features = {}
    for title in summary:
        # positive semantic list
        positive_semantic_list = []
        # negative semantic list
        negative_semantic_list = []
        # positive feautures list
        positive_features_list = []
        # negative feautures list
        negative_features_list = []
        for each_pair in summary[title]:
            flag = False
            descriptor = each_pair[0]
            feature = each_pair[1]
            if lang == 'fr':
                pair_sentiment = pattern.fr.sentiment(descriptor+" "+feature)
                if pair_sentiment[0] >= 0.2 and pair_sentiment[1] >= 0.2:
                    positive_features_list.append((descriptor, feature))
                    proc = subprocess.Popen(["java", "-jar", "./disco-2.1.jar", "./fr-general-20151126-lm-sim", "-s",descriptor.encode('utf-8'), feature.encode('utf-8'), 'COSINE'], stdout=subprocess.PIPE, shell=False)
                    (out, err) = proc.communicate()
                    if out.startswith("Err"):
                        out = 0.0
                    positive_semantic_list.append(float(out))


                elif pair_sentiment[0] <= -0.2 and pair_sentiment[1] > 0.2:
                    negative_features_list.append((descriptor, feature))
                    proc = subprocess.Popen(["java", "-jar", "./disco-2.1.jar", "./fr-general-20151126-lm-sim", "-s",descriptor.encode('utf-8'), feature.encode('utf-8'), 'COSINE'], stdout=subprocess.PIPE, shell=False)
                    (out, err) = proc.communicate()
                    if out.startswith("Err"):
                        out = 0.0
                    negative_semantic_list.append(float(out))


            elif lang == 'de':
                pair_sentiment = TextBlob(descriptor+" "+feature).sentiment
                if pair_sentiment[0] >= 0.5:
                    positive_features_list.append((descriptor, feature))
                    proc = subprocess.Popen(["java", "-jar", "./disco-2.1.jar", "./de-general-20150421-lm-sim", "-s",descriptor.encode('utf-8'), feature.encode('utf-8'), 'COSINE'], stdout=subprocess.PIPE, shell=False)
                    (out, err) = proc.communicate()
                    if out.startswith("Err"):
                        out = 0.0
                    positive_semantic_list.append(float(out))
                elif pair_sentiment[0] <= 0.5:
                    negative_features_list.append((descriptor, feature))
                    proc = subprocess.Popen(["java", "-jar", "./disco-2.1.jar", "./de-general-20150421-lm-sim", "-s",descriptor.encode('utf-8'), feature.encode('utf-8'), 'COSINE'], stdout=subprocess.PIPE, shell=False)
                    (out, err) = proc.communicate()
                    if out.startswith("Err"):
                        out = 0.0
                    negative_semantic_list.append(float(out))

        sorted_positive_index = sorted(range(len(positive_semantic_list)), key=lambda k: positive_semantic_list[k], reverse = True)
        sorted_negative_index = sorted(range(len(negative_semantic_list)), key=lambda k: negative_semantic_list[k], reverse = True)
            # display all the feature pairs along with the sentiments
        new_positive_feature_list = []
        new_negative_feature_list = []
        if len(positive_features_list) != 0 or len(negative_features_list) != 0:
            print(title)
            if len(positive_features_list) != 0:
                print
                print("Positive Reviews:")
                for i in range(0, len(positive_semantic_list)):
                    new_positive_feature_list.append(positive_features_list[sorted_positive_index[i]])
                    print(positive_features_list[sorted_positive_index[i]][0].encode('utf-8')+" "+positive_features_list[sorted_positive_index[i]][1].encode('utf-8'))
                print
            if len(negative_features_list) != 0:
                print("Negative Reviews:")
                for i in range(0, len(negative_features_list)):
                    new_negative_feature_list.append(negative_features_list[sorted_negative_index[i]])
                    print(negative_features_list[sorted_negative_index[i]][0].encode('utf-8')+" "+negative_features_list[sorted_negative_index[i]][1].encode('utf-8'))
                print

            final_features[title] = [new_positive_feature_list, new_negative_feature_list]
    return(final_features)



if __name__ == '__main__':
    summary = open(sys.argv[1])
    [books_summary, dvd_summary, music_summary] = json.load(summary)
    summary.close()
    books_final_features = []
    dvd_final_features = []
    music_final_features = []
    os.makedirs("Summary")

    for each in books_summary:
        if each[0] == "fr":
            books_outFile = open("Summary/Books_Summarized_Reviews_fr.txt", 'w')
        elif each[0] == "de":
            books_outFile = open("Summary/Books_Summarized_Reviews_de.txt", 'w')
        summary = sentiment_analyser(each[1], each[0])

        for title in summary:
            books_outFile.write(title.encode("utf-8"))
            books_outFile.write("\n-------------------------------------------------------------------\n")


            if len(summary[title][0]) > 0:
                books_outFile.write("\n\nPositive Reviews\n")
                books_outFile.write("--------------------\n")
            for feature in summary[title][0]:
                books_outFile.write(feature[0].encode("utf-8") + " " + feature[1].encode("utf-8"))
                books_outFile.write("\n")

            if len(summary[title][1]) > 0:
                books_outFile.write("\nNegative Reviews\n")
                books_outFile.write("--------------------\n")
            for feature in summary[title][1]:
                books_outFile.write(feature[0].encode("utf-8") + " " + feature[1].encode("utf-8"))
                books_outFile.write("\n")

            books_outFile.write("\n")


    for each in dvd_summary:
        if each[0] == "fr":
            dvd_outFile = open("Summary/DVDs_Summarized_Reviews_fr.txt", 'w')
        elif each[0] == "de":
            dvd_outFile = open("Summary/DVDs_Summarized_Reviews_de.txt", 'w')
        summary = sentiment_analyser(each[1], each[0])

        for title in summary:
            dvd_outFile.write(title.encode("utf-8"))
            dvd_outFile.write("\n-------------------------------------------------------------------\n")

            if len(summary[title][0]) > 0:
                dvd_outFile.write("\n\nPositive Reviews\n")
                dvd_outFile.write("--------------------\n")
            for feature in summary[title][0]:
                dvd_outFile.write(feature[0].encode("utf-8")+"-"+ feature[1].encode("utf-8"))
                dvd_outFile.write("\n")

            if len(summary[title][1]) > 0:
                dvd_outFile.write("\nNegative Reviews\n")
                dvd_outFile.write("--------------------\n")
            for feature in summary[title][1]:
                dvd_outFile.write(feature[0].encode("utf-8")+"-"+ feature[1].encode("utf-8"))
                dvd_outFile.write("\n")

            dvd_outFile.write("\n")


    for each in music_summary:
        if each[0] == "fr":
            music_outFile = open("Summary/Music_Summarized_Reviews_fr.txt", 'w')
        elif each[0] == "de":
            music_outFile = open("Summary/Music_Summarized_Reviews_de.txt", 'w')
        summary = sentiment_analyser(each[1], each[0])

        for title in summary:
            music_outFile.write(title.encode("utf-8"))
            music_outFile.write("\n-------------------------------------------------------------------\n")

            if len(summary[title][0]) > 0:
                music_outFile.write("\n\nPositive Reviews\n")
                music_outFile.write("--------------------\n")
            for feature in summary[title][0]:
                music_outFile.write(feature[0].encode("utf-8")+" "+ feature[1].encode("utf-8"))
                music_outFile.write("\n")

            if len(summary[title][1]) > 0:
                music_outFile.write("\nNegative Reviews\n")
                music_outFile.write("--------------------\n")
            for feature in summary[title][1]:
                music_outFile.write(feature[0].encode("utf-8")+" "+ feature[1].encode("utf-8"))
                music_outFile.write("\n")

            music_outFile.write("\n")
