import pymongo
client = pymongo.MongoClient('localhost',27017)
db = client['test']

#db_sa = db['SummarizedArticle']
def addKeywords(keyword_list):
    items = db.SummarizedArticle.find({})
    keywords = set()
    for i in items:
        kws = i['keywords']
    #    print type(kws)
        for entry in kws:
            keywords.add(entry)
    for kw in keyword_list:
        keywords.add(kw)
    #print keywords
    l=list(keywords)
    print len(l)
    db.Keyword.drop()
    db.Keyword.insert({"id":'1',"keywords":l})
    client.close()
    #print type(items)
    #print items

