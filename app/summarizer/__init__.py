#*- coding: utf-8 -*-
from flask import Blueprint

summarizer_blueprint = Blueprint('summarizer', __name__)


from .feature_extractor_article_based import get_complete_feature_vector
from .neural_network_script import Neural_Network
from . import routes
from .split import split_into_sentences