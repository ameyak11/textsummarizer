#*- coding: utf-8 -*-
import re

##
caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr|Rs|Col|www|Prof)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
num = "([0-9])"
##


def split_into_sentences(text):
    # split text into sentences
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(num + "[.]" + num, "\\1<prd>\\2", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    if "a.m." in text: text = text.replace("a.m.", "a<prd>m<prd>")
    if "p.m." in text: text = text.replace("p.m.", "p<prd>m<prd>")
    if "i.e." in text: text = text.replace("i.e.", "i<prd>e<prd>")
    text = re.sub("\s" + caps + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + caps + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    p=re.compile(ur'\xe2\x80\x9c(.+?)\xe2\x80\x9d',re.UNICODE)
    list_q = p.findall(text)
    # print "len of list",len(list_q)
#   print "\n"
    for entry in list_q:
        temp =entry
        if "." in entry:
#           print "in if"
            entry = entry.replace(".","<diq>")
            entry = entry.replace("?","<qiq>")
            entry = entry.replace("!","<eiq>")
#           print "entry:",entry
            text = text.replace(temp,entry)
#           print " in if ",text
#           print "\n"
#   print "text before"+text
#   print "after"
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<diq>",".")
    text = text.replace("<qiq>","?")
    text = text.replace("<eiq>","!")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    # print "type(sentences): ",type(sentences)
    print "number of sentences: ",len(sentences)
    return sentences