""" 
Code implements feature extraction of following features :

f1	= Sentence position
	= first five sentences have more weightage 
	= 5/5 for 1st sentence 4/5 for 2nd ... 1/5 for 5th.. 0 for rest

f4 	= Sentence centrality 
	= |keywords in s | / |keywords in s U keywords in other sentences|

f5 	= Sentence resemblance with title
	= |keywords in s (intersection) keywords in title | / |keywords in s U keywords in title|

f6	= Sentence inclusion of named entity
	= #(Proper Nouns in s) / len(s)

f7 	= Sentence inclusion of numerical_data
	= #(numerical_data in s) / len(s)

f8 	= Sentence relative length
	= len(s)*average_sentence_length

Features f9 and f10 are based on similarity graph used in bushy path method

f9	= #(branches connected to the node)
	= Number of branches with non-zero weight

f10	= Aggregate similarity
	= Summation of weights of the similarity graph

article_feature_set is the matrix to be given to the neural network as input feature_set
"""

import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re


stops = set(stopwords.words("english"))
vectorizer = CountVectorizer(analyzer = "word",
	tokenizer=None,
	preprocessor=None,
	stop_words=None,
	max_features= None)


def f1(lines):
    # print "Inside f1"
    f1=np.zeros(len(lines))
    index = int(5)
    for i in range(len(lines)):
		#print "f1--->"+str((float(index)/float(5)))
		f1[i]=((float(index)/float(5)))
		index = index-1
		if index == -1:
			index = 0
    return f1


def f4(feature_vector_matrix):
	# print "Inside f4"
	keywords_in_line = np.sum(feature_vector_matrix[1:],axis=1)
	f4=np.zeros(len(keywords_in_line))
	#print keywords_in_line
	total_keyword_count = len(feature_vector_matrix[0])
	#print " Number of keywords -- "+ str(total_keyword_count)
	for i in range(len(keywords_in_line)):
		f4[i] = float(keywords_in_line[i]) / float(total_keyword_count)
	return f4


def f5(feature_vector_matrix):
    # print "Inside f5"
    f5 = np.zeros(len(feature_vector_matrix)-1)
    index=0
    for line in feature_vector_matrix[1:]:
        f5[index] = (float(sum(feature_vector_matrix[0]
		    & line))
	    / float(sum(feature_vector_matrix[0]
		    | line)))
        index = index+1
    return f5


def f6f7f8(lines):
    # print "Inside f6f7f8"
    f6 = np.zeros(len(lines))
    f7 = np.zeros(len(lines))
    f8 = np.zeros(len(lines))
	#get lines containing proper nouns
    tagged_lines = []		# used only for testing remove from final code
    sentence_lengths = []
    for l in range(len(lines)):
        numerical_data = re.findall(r'\d+\.\d+|\d+(?:\,\d+)*',lines[l])
        len_l = len(lines[l].split())
        if len_l!=0:
            f7[l] = (float(len(numerical_data))/float(len_l))
            #print "f7--->" + str(float(len(numerical_data))/float(len_l))
            sentence_lengths.append(len_l)
            ln = pos_tag(lines[l].split())
            nnp_count = int(0)		#count of proper nouns
            for w,tag in ln:
                if tag == 'NNP':
                    nnp_count = nnp_count+1
            f6[l] = (float(nnp_count)/float(len_l))
            #print "f6--->"+str(float(nnp_count)/float(len_l))
            tagged_lines.append(ln)
        else:
            f7[l]=0.0
            f6[l]=0.0
    sentence_lengths = np.array(sentence_lengths)
    #print sentence_lengths
    if(float(len(sentence_lengths))!=0):
        average_length = float(sum(sentence_lengths))/float(len(sentence_lengths))
        # print average_length
        for index in range(len(sentence_lengths)):
            f8[index] = (float(sentence_lengths[index]) * float(average_length))
            # print "f8--->"+str(float(sentence_lengths[index])*average_length)
    else:
        for index in range(len(sentence_lengths)):
            f8[index] = 20
            # print "f8--->"+str(float(sentence_lengths[index])*average_length)
    return f6,f7,f8


def f9f10(lines_without_stopwords,feature_set):
    # print "Inside f9f10"
    dimension = len(feature_set)
    graph = np.zeros((dimension,dimension))
    for row in range(dimension):
        current_line = feature_set[row]
        for col in range(dimension):
            if(row == col):
                continue
            line = feature_set[col]
            val = (float(sum(line & current_line))
                / (np.log10(len(lines_without_stopwords[row].split()))
                    + np.log10(len(lines_without_stopwords[col].split()))))
            graph[row][col] = val
    #print graph
    f9 = np.zeros(dimension)
    for row in range(dimension):
        f9[row]=(np.count_nonzero(graph[row]))
    #print "f9--->",f9
    f10 = np.sum(graph,axis=1)
    #print "f10--->",f10
    return f9,f10


def entry_func(lines,lines_without_stopwords,feature_vector_matrix,article_feature_set):
    lines = lines[1:]       #ommit title from lines array
    article_feature_set[1]=f4(feature_vector_matrix)
    article_feature_set[2]=f5(feature_vector_matrix)
    f6, f7, f8 = f6f7f8(lines)
    article_feature_set[3]=f6
    article_feature_set[4]=f7
    article_feature_set[5]=f8
    article_feature_set[0]=f1(lines)
    f9,f10 = f9f10(lines_without_stopwords,feature_vector_matrix[1:])    #feature vector matriz is given to f9f10 without row for title
    article_feature_set[6]=f9
    article_feature_set[7]=f10
    article_feature_set = article_feature_set.transpose()
    return article_feature_set

def initialize():
    lines = open("/home/ameya/Desktop/news000.txt").readlines()
    lines_without_stopwords = []
    for l in lines:
	    #l=l.split()
            l = nltk.word_tokenize(l)
	    mw = [w for w in l if w not in stops]
	    l = (" ".join(mw))
	    lines_without_stopwords.append(l)

    lines_without_stopwords = lines_without_stopwords[1:]
    #print lines_without_stopwords[len(lines_without_stopwords)-1]

    feature_vector_matrix = vectorizer.fit_transform(lines_without_stopwords)
    feature_vector_matrix = feature_vector_matrix.toarray()
    #print feature_vector_matrix.shape
    #print feature_vector_matrix
    vocab = vectorizer.get_feature_names()
    #print vocab
    article_feature_set = np.zeros((10,len(feature_vector_matrix)-1))
    article_feature_set = entry_func(lines,lines_without_stopwords,feature_vector_matrix,article_feature_set)
    print article_feature_set #article_feature_set is the input matrix to be given to the neural network


def get_complete_feature_vector(inputlines):
    # print "Inside get_complete_feature_vector"
    lines = inputlines
    lines_without_stopwords = []
    for l in lines:
        # l=l.split()
        l = nltk.word_tokenize(l)
        mw = [w for w in l if w not in stops]
        l = (" ".join(mw))
        lines_without_stopwords.append(l)

    feature_vector_matrix = vectorizer.fit_transform(lines_without_stopwords)
    feature_vector_matrix = feature_vector_matrix.toarray()
    vocab = vectorizer.get_feature_names()
    article_feature_set = np.zeros((8, len(feature_vector_matrix) - 1))
    article_feature_set = entry_func(lines, lines_without_stopwords, feature_vector_matrix, article_feature_set)
    # print "Feature vector shape ", article_feature_set.shape
    # print "Returning from get_complete_feature_vector"
    print article_feature_set
    return article_feature_set


if __name__ == '__main__':
    initialize()



