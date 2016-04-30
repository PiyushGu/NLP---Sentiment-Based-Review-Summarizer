'''
Python program used to find the frequent item set by implementing A-Priori
'''

import sys
import itertools
files=sys.argv

def apriori():
    basket_items=[]
    set_items=set()
    lines=[l.rstrip() for l in open(files[1],'r')]
    
    
    #Spliting the line with delimeter = ','
    for line in lines:
        basket_items.append(line.split(','))
    for basket in basket_items:
        for item in basket:
            set_items.add(item)
    unique_items=sorted(set_items)
    dict_item={}
    for item in unique_items:
        dict_item[item]=0
    for basket in basket_items:
        for item in basket:
            dict_item[item]+=1
    freq_item=[[]]
    for item in dict_item:
        if dict_item[item]>=int(files[2]):
            freq_item[0].append(item)

    print("Frequent itemsets of size 1")
    for i,eachitem in enumerate(freq_item[0]):
        print(freq_item[0][i])
    cand_items=[]
    k=0
    
    
    while('true'):
        freq_item.append([])
        cand_items.append([])
        for item in list(itertools.combinations(freq_item[0],k+2)):
            if (k+2)==2:
                item=sorted(item)
                cand_items[k].append(item)
            else:
                count=0
                for items in list(itertools.combinations(item,k+1)):
                    items=sorted(items)
                    if items in freq_item[k]:
                        count+=1
                if count==(k+2):
                    item=sorted(item)
                    cand_items[k].append(item)
                

        count=[0]*len(cand_items[k])
        for basket in basket_items:
            for index,each_item in enumerate(cand_items[k]):
                if [i for i in each_item for b_item in basket if i==b_item]==list(each_item):
                    count[index]+=1
        for i in range(len(count)):
            if count[i]>=int(files[2]):
                freq_item[k+1].append(cand_items[k][i])
                
        if not freq_item[k+1]:
            break
        else:
            print("\nFrequent itemsets of size %d"%(k+2))
            for eachitem in freq_item[k+1]:
                out=''
                eachitem=list(eachitem)
                for item in eachitem:
                    out+=''.join(item)+','
                out=out.rstrip(',')
                print(out)
        k+=1

                            
apriori()
