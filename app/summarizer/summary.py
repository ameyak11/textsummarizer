# from .split import split_into_sentences
# from .feature_extractor_article_based import get_complete_feature_vector
# from .neural_network_script import Neural_Network
#from .bushy_path import initialize
#from .keywords import addKeywords


# def getUnSummarizedArticles():
#     session = Session.connect(MONGOALCHEMY_DATABASE)
#     count  = session.query(Article).filter(Article.summarized == False).count()
#     if count == 0:
#         pass
#     else:
#         articles = session.query(Article).filter(Article.summarized == False)
#         return articles
#     session.end()
#     return 0


# def summarizeNews():
#     articles = getUnSummarizedArticles()
#     keyword_set = set()
#     if articles == 0:
#         pass
#     else:
#         session = Session.connect(MONGOALCHEMY_DATABASE)
#         NN = Neural_Network()
#         for entry in articles:
#             lines = list()
#             title = entry.title
#             print title
#             print entry.link_article
#             content = entry.content
#             sentences = split_into_sentences(content)
#             if len(sentences)>5:
#                 lines.append(title)
#                 lines = lines + sentences
#                 feature_vector = get_complete_feature_vector(lines)
#                 summary_indices = NN.get_summary(feature_vector)
#                 keywords = initialize(sentences)
#                 # print type(keywords)
#                 # print "keywords: ", keywords
#                 # print "summary indices: ",summary_indices
#                 # print "Length of article: ",len(sentences)
#                 # print "Length of summary: ",len(summary_indices)
#                 print "\n"
#                 # print entry.link_image
#                 summary_sentences = ''
#                 for item in summary_indices:
#                     summary_sentences += sentences[item]
#                 # print summary_sentences
#                 # print "types"
#                 # print type(entry.category)
#                 # print type(entry.publisher)
#                 # print type(entry.title)
#                 # print type(entry.date)
#                 # print type(summary_sentences)
#                 # print type(keywords)
#                 # print type(entry.link_article)
#                 # print type(entry.link_image)

#                 news = SummarizedArticle(category = entry.category,
#                                          publisher = entry.publisher,
#                                          title = entry.title,
#                                          date = entry.date,
#                                          content = summary_sentences,
#                                          keywords = keywords,
#                                          link_article = entry.link_article,
#                                         link_image = entry.link_image,
#                                         tweetIsPresent = entry.tweetIsPresent,
#                                         tweetLinks = entry.tweetLinks)
#                 for i in keywords:
#                     keyword_set.add(i)
#             else:
#                 summary_sentences=''
#                 for item in sentences:
#                     summary_sentences += item
#                 news = SummarizedArticle(category=entry.category,
#                                          publisher=entry.publisher,
#                                          title=entry.title,
#                                          date=entry.date,
#                                          content=summary_sentences,
#                                          link_article=entry.link_article,
#                                          link_image=entry.link_image,
#                                          tweetIsPresent=entry.tweetIsPresent,
#                                          tweetLinks=entry.tweetLinks)
#             session.save(news)
#             update_status = session.query(Article).filter(Article.link_article==entry.link_article)
#             print update_status.count()
#             update_status.set(summarized=True).execute()
#             addKeywords(keyword_set)
#         # for k in keyword_set:
#         #     keyword_query = session.query(SummarizedArticle).filter(Keyword.id == '1')
#         #     keyword_query.add_to_set(Keyword.id=='1', k).execute()
#         session.end()



# @celery.task(name='summary.summarizeDriver')
# def summarizeDriver():
#     summarizeNews()


