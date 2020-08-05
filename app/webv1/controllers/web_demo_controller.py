from flask import jsonify, request
from functools import update_wrapper
from datetime import timedelta
from flask import make_response, request, current_app
from bson import ObjectId

from ..forms import PostDemoArticleForm
from ...webv1 import webv1 as webv1
from ...summarizer.feature_extractor_article_based import get_complete_feature_vector
from ...summarizer.neural_network_script import Neural_Network
from ...summarizer.split import split_into_sentences
from ...summarizer.bushy_path import initialize

from ...models import DemoSummarizerArticle

import json
import datetime
import re
import requests

from flask import render_template

#myAPIKey = "Akr1wvrEY6qao9vrZN5LxenFvroup0EvrevEiXRWsQ8QkgUz"
#API_URL = 'https://mercury.postlight.com/parser'
# test_url = "http://indianexpress.com/article/india/manohar-parrikar-swearing-in-ceremony-goa-takes-oath-nine-mlas-bjp-floor-test-congress-4568822/"

log_file = "web_log.txt"
"""
Decorator for cross - site resouce scrpit
"""


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


def custom_error(error):
    return jsonify(error)


# functions to make call to mercury API to get content of url given by user for summarization


def getKey():
    return re.sub('vr', '', myAPIKey)


def makeAPIRequest(url, key):
    payload = {'url': url}
    headers = {'Content-Type': 'application/json', 'x-api-key': key}
    r = requests.get(url=API_URL, headers=headers, params=payload, verify=True)
    print r.json()
    return r.json()


# route to test working of server


@webv1.route('/test_demo', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', headers=['Authorization', 'Content-Type'])
def newstest():
    return jsonify("WEB DEMO working")


# route to summarize the input article using x-www-form-urlencoded data


@webv1.route('/summarizef', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['Authorization', 'Content-Type'])
def summarize_given_newsf():
    form = PostDemoArticleForm(request.form)
    if form.validate():
        NN = Neural_Network()
        article_title = form.article_title.data
        article_body = form.article_body.data
        lines = list()
        print article_title, article_body
        sentences = split_into_sentences(article_body)
        lines.append(article_title)
        lines = lines + sentences
        feature_vector = get_complete_feature_vector(lines)
        summary_indices = NN.get_summary(feature_vector)
        return jsonify(article_title=article_title, article_body=sentences, summary_indices=summary_indices)
    else:
        return jsonify(form.errors), 400


# route to summarize the input article using form-data


@webv1.route('/summarize_article', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def summarize_given_news():
    fp = open(log_file, 'a')
    NN = Neural_Network()
    fp.write("\n---------------------------------\n")
    article_title = request.form['article_title']
    article_body = request.form['article_body']
    fp.write("Summarizating article : " + article_title + "\n")
    lines = list()
    print article_title, article_body
    sentences = split_into_sentences(article_body)
    lines.append(article_title)
    lines = lines + sentences
    feature_vector = get_complete_feature_vector(lines)
    summary_indices = NN.get_summary(feature_vector)
    ##-----------
    keywords = initialize(sentences)
    # print type(keywords)
    ##---------------
    fp.write("Summary generated successfully\n")
    summary = ""
    for i in summary_indices:
        summary = summary + sentences[i]
    new_article = DemoSummarizerArticle()
    fp.write("Generated demo summarized article object\n")
    new_article.title = article_title
    new_article.article_body = sentences
    new_article.article_summary = summary
    new_article.summary_indices = summary_indices
    # new_article.save()
    fp.write("Saved demo summarized article object\n Returning json\n")
    fp.close()
    return jsonify(new_article.get_dict())


# route to summarize article using url


@webv1.route('/summarize_link', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def summarize_given_url():
    fp = open(log_file, 'a')
    NN = Neural_Network()
    article_link = request.form['article_link']
    fp.write("\n---------------------------------\n")
    fp.write("Summarizating link : "+article_link+"\n")
    response = makeAPIRequest(article_link, getKey())
    if response is None:
        fp.write("API CALL unsuccessful\n")
        fp.close()
        article_body = []
        article_body.append("Please Enter a valid URL")
        summary_indices = []
        summary_indices.append("0")
        return jsonify(_id="garbage_id", article_title="Invalid URL", article_body=article_body,
                       summary_indices=summary_indices)
    fp.write("API CALL successful\n")
    print response['title']
    print response['content']
    article_title = response['title']
    text = response['content']
    text = re.sub('<.*?>', '', text)
    article_body = text
    lines = list()
    print article_title, article_body
    sentences = split_into_sentences(article_body)
    lines.append(article_title)
    lines = lines + sentences
    feature_vector = get_complete_feature_vector(lines)
    summary_indices = NN.get_summary(feature_vector)
    fp.write("Summary generated successfully\n")
    summary = ""
    for i in summary_indices:
        summary = summary + sentences[i]
    new_article = DemoSummarizerArticle()
    fp.write("Generated demo summarized article object\n")
    new_article.link_article = article_link
    new_article.title = article_title
    new_article.article_body = sentences
    new_article.article_summary = summary
    new_article.summary_indices = summary_indices
    #new_article.save()
    #fp.write("Saved demo summarized article object\n Returning json\n")
    fp.close()
    return jsonify(new_article.get_dict())




#route to return demo
@webv1.route('/demo', methods=['GET'])
@crossdomain(origin='*')
def show_demo():
    return render_template('index.html', title='Demo')


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o.strftime("%Y-%m-%d %H:%M:%S"))
        return json.JSONEncoder.default(self, o)
