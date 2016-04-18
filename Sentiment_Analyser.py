import sys, json
import pattern.fr
from textblob_de import TextBlobDE as TextBlob
import subprocess
import os
from multiprocessing import pool

def sentiment_analyser(summary, lang):
    for title in summary:
        positive_semantic_list = []
        negative_semantic_list = []
        positive_features_list = []
        negative_features_list = []
        for each_pair in summary[title]:
            flag = False
            descriptor = each_pair[0]
            feature = each_pair[1]
            if lang == 'fr':
                pair_sentiment = pattern.fr.sentiment(descriptor+" "+feature)
                if pair_sentiment[0] >= 0.2 and pair_sentiment[1] >= 0.2:
                    positive_features_list.append((descriptor, feature))
                    proc = subprocess.Popen(["java", "-jar", "./disco-2.1.jar", "./fr-general-20151126-lm-sim", "-s2",descriptor.encode('utf-8'), feature.encode('utf-8'), 'KOLB'], stdout=subprocess.PIPE, shell=False)
                    (out, err) = proc.communicate()
                    positive_semantic_list.append(out)

                elif pair_sentiment[0] <= -0.2 and pair_sentiment[1] > 0.2:
                    negative_features_list.append((descriptor, feature))
                    proc = subprocess.Popen(["java", "-jar", "./disco-2.1.jar", "./fr-general-20151126-lm-sim", "-s2",descriptor.encode('utf-8'), feature.encode('utf-8'), 'KOLB'], stdout=subprocess.PIPE, shell=False)
                    (out, err) = proc.communicate()
                    negative_semantic_list.append(out)

            elif lang == 'de':
                pair_sentiment = TextBlob(descriptor+" "+feature).sentiment
                if pair_sentiment[0] >= 0.5:
                    positive_features_list.append((descriptor, feature))
                elif pair_sentiment[0] <= 0.5:
                    negative_features_list.append((descriptor, feature))

        sorted_positive_index = sorted(range(len(positive_semantic_list)), key=lambda k: positive_semantic_list[k])
        sorted_negative_index = sorted(range(len(negative_semantic_list)), key=lambda k: negative_semantic_list[k])
            # display all the feature pairs along with the sentiments
        if len(positive_features_list) != 0 or len(negative_features_list) != 0:
            print(title)
            if len(positive_features_list) != 0:
                print
                print("Positive Reviews:")
                for i in range(0,len(positive_semantic_list)):
                    print(positive_features_list[sorted_positive_index[i]][0].encode('utf-8')+" "+positive_features_list[sorted_positive_index[i]][1].encode('utf-8'))
                print
            if len(negative_features_list) != 0:
                print("Negative Reviews:")
                for i in range(0,len(negative_features_list)):
                    print(negative_features_list[sorted_negative_index[i]][0].encode('utf-8')+" "+negative_features_list[sorted_negative_index[i]][1].encode('utf-8'))
                print

# def func(summary):
#     for each in summary:
#         my_summary=sentiment_analyser(each[1],each[0])



if __name__ == '__main__':
    summary = open(sys.argv[1])
    [books_summary, dvd_summary, music_summary] = json.load(summary)
    summary.close()

    for each in books_summary:
        print("Books Summary for "+each[0]+" language")
        summary = sentiment_analyser(each[1], each[0])
    #     # books_summary.append((each[0], summary))
    #
    for each in dvd_summary:
        print("DVD Summary for "+each[0]+" language")
        summary = sentiment_analyser(each[1], each[0])
    #     # dvd_summary.append((each[0], summary))

    for each in music_summary:
        print("Music Summary for "+each[0]+" language")
        summary = sentiment_analyser(each[1], each[0])
        # music_summary.append((each[0], summary))
