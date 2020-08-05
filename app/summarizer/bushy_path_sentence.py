"""
Unsupervised summarization technique : bushy path algorithm
Code for generating bushy path considering sentences as nodes

Node Value
WS(Vi) = (1-d) + d * sum( (wij / sum( wjk ) for all k E out(Vj)) * WS(Vj) for all j E in(Vi))

d = 0.85
convergence threshold = 0.0001

"""

import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
from collections import OrderedDict

stops = set(stopwords.words("english"))
vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer=None,
                             preprocessor=None,
                             stop_words=None,
                             max_features= None)


def initialize(lines):
    # lines = open("/home/ameya/Desktop/news000.txt").readlines()
    # lines = lines[2:]	#Ommit link and title
    lines_without_stopwords = []
    for l in lines:
        l= nltk.word_tokenize(l)
        mw = [w for w in l if w not in stops]
        l = (" ".join(mw))
        lines_without_stopwords.append(l)
    print lines_without_stopwords

    feature_vector_matrix = vectorizer.fit_transform(lines_without_stopwords)
    feature_vector_matrix = feature_vector_matrix.toarray()
    print feature_vector_matrix.shape
    vocab = vectorizer.get_feature_names()
    print vocab
    return lines_without_stopwords,feature_vector_matrix

def create_sentence_graph(lines_without_stopwords,feature_set):
    dimension = len(feature_set)
    graph = np.zeros((dimension,dimension))
    #print graph
    for row in range(dimension):
        current_line = feature_set[row]
        print "Selected line : {}".format(lines_without_stopwords[row])
        for col in range(dimension):
            if(row == col):
                continue
            line = feature_set[col]
            print "------"
            print lines_without_stopwords[col]
            print float(sum(line & current_line))
            print len(lines_without_stopwords[row].split()),np.log10(len(lines_without_stopwords[row].split()))
            print len(lines_without_stopwords[col].split()),np.log10(len(lines_without_stopwords[col].split()))    
            val = (float(sum(line & current_line)) 
                   / (np.log10(len(lines_without_stopwords[row].split()))
                      + np.log10(len(lines_without_stopwords[col].split()))))
            print val
            print "------##------"
            graph[row][col] = val
    print graph
    summation_array = np.sum(graph,axis=1)
    print summation_array
    return graph,summation_array 

def bushy_path_algorithm(graph,summation_array):
    print "Inside bushy_path_algorithm"
    #constants
    d =float(0.85)
    c = 1-d
    threshold = float(0.0001)
    flag = True
    iterations = 1
    WS = np.ones(len(graph))	#WS value for each sentence
    while flag:
        print iterations
        for w in range(len(WS)):
            summation = 0.0
            for node in range(len(graph)):
                inner_summation = graph[w][node]/summation_array[node]
                node_value = inner_summation*WS[node]
                summation = summation+node_value
            value = c + d*summation
            if(abs(value - WS[w]) <= threshold):
                flag = False
            else:
                flag = True
            WS[w] = value
        iterations += 1
    print WS
    return WS

# def main():
def unsupervised_summary(lines):
    lines_without_stopwords,feature_set = initialize(lines)
    graph,summation_array = create_sentence_graph(lines_without_stopwords,feature_set)
    WS = bushy_path_algorithm(graph,summation_array)
    print "Graph:"
    # print graph
    print "Values:"
    # print WS
    finalsummary = dict()
    for w in range(len(WS)):
        finalsummary[WS[w]] = lines_without_stopwords[w]
    print finalsummary
    summary = sorted(finalsummary.items(),reverse=True)
    compression = (3.0/10.0)*len(WS)
    print compression
    for i in range(int(compression)):
        print summary[i]
'''
if __name__ == '__main__':
    main()
'''
