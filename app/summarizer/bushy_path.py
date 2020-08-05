"""
KeyWord Extraction code completed
Code implements the formation of bushy path of text

1. keyword extraction 

Node value
S(Vi) = (1-d) + d * sum( ( 1 / |Out(Vj)| ) * S(Vj) ) for all j E In(Vi)

d = 0.85
convergence threshold = 0.0001

Parts of speech considered - Nouns and Adjectives
*** Consideration of Adjectives yet to be finalized ***

Title not considered for keyword extraction
"""

import nltk
import re
from nltk.tag import pos_tag
from collections import OrderedDict

filepath = "/home/ameya/Desktop/news000.txt"

def find_nouns_adjectives(clear_lines):
    print "Inside find_nouns_adjectives"
    tagged_lines = []
    adjectives = []
    nouns = []
    for l in clear_lines:
        l = pos_tag(l)
        for w,tag in l:
            if ((tag == 'NN' or tag == 'NNS' or tag == 'NNP' or tag == 'NNPS') and (w not in nouns)):
                nouns.append(w)
            if ((tag == 'JJ' or tag == 'JJR' or tag == 'JJS') and (w not in adjectives)):
                adjectives.append(w)
        tagged_lines.append(l)
    print "Adjectives"
    print adjectives
    print "Nouns"
    print nouns
    print "Exiting find_nouns_adjectives"
    return nouns,adjectives

def create_graph(clear_lines,adjectives,nouns):
    print "Inside create_graph"
    graph = dict()
    for w in nouns:
        graph[w] = {'s':float(1),'n':[]}
    #print graph.keys()
    for l in clear_lines:
        count = len(l)-1
        for i in range(0,count):
            if l[i] in graph.keys() and l[i+1] in graph.keys():
                #print l[i]+"---"+l[i+1]
                if l[i+1] not in graph[l[i]]['n']:
                    graph[l[i]]['n'].append(l[i+1])
                if l[i] not in graph[l[i+1]]['n']:
                    graph[l[i+1]]['n'].append(l[i])
    #print graph
    print len(graph.keys())
    for key in graph.keys():
        if not graph[key]['n']:
            del graph[key]
    print len(graph.keys())			#removed nodes that have no links
    print "Exiting create_graph"
    return graph

def bushy_path_algo(graph):
    print "Inside bushy_path_algo"
    #constants
    d = float(0.85)
    c = 1-d
    threshold = float(0.0001)
    print graph.keys()
    flag = True
    iterations = 1
    while flag:
        print iterations
        # print graph['temple']
        for v in graph.keys():		#v = vertex
            summation = 0.0
            #print graph[graph[v]['n'][0]]['s']
            #print graph[graph[v]['n'][0]]['n']
            for w in graph[v]['n']:
                summation += graph[w]['s']/float(len(graph[w]['n']))
            val = c + d*summation
            #print val
            if (abs(val - graph[v]['s']) <= threshold):
                flag = False
            else:
                flag = True
            graph[v]['s'] = val
        iterations += 1
    final_graph = OrderedDict(sorted(graph.iteritems(),key = lambda x: x[1]['s'],reverse = True))
    print final_graph.keys()
    print "Exiting bushy_path_algo"
    return final_graph.keys()[:5]


def initialize(lines):
    print "Inside initialize"
    # lines = open(filepath).readlines()
    # lines = lines[2:]		#Ommit link and title
    clear_lines = []
    nouns = []
    adjectives = []
    #print nltk.pos_tag(nltk.word_tokenize(lines[0]))
    for l in lines:
        print l
        l = re.sub('[^a-zA-Z0-9\n\.\- ]', '', l)
        l = nltk.word_tokenize(l)
        places = []
        length_l = len(l)
        for i in range(0, length_l):
            print i
            if l[i] == "-":
                if i != 0 and i != len(l) - 1 and i != len(l) - 2:
                    l[i - 1] = l[i - 1] + l[i] + l[i + 1]
                    places.append(i)
        print places

        for i in range(0, len(places)):
            del l[places[i]-i*2]
            del l[places[i]-i*2]
        l = l[:-1]
        clear_lines.append(l)
    nouns,adjectives = find_nouns_adjectives(clear_lines)
    graph = create_graph(clear_lines,adjectives,nouns)
    keywords = bushy_path_algo(graph)
    upper_keywords = []
    for k in keywords:
        upper_keywords.append(k.upper())
    return upper_keywords

# initialize()
