from elasticsearch import Elasticsearch

from semantic_labeling.search.indexer import Indexer
from semantic_labeling.search.searcher import Searcher

__author__ = 'alse'
elastic_search = Elasticsearch()
indexer = Indexer(elastic_search)
searcher = Searcher(elastic_search)
