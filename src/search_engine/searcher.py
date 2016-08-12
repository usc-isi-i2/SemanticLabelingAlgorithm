from collections import defaultdict

import pandas as pd
from elasticsearch.helpers import scan

from search_engine import es
from semantic_labeling import TF_TEXT, data_collection, relation_collection, coop_collection


class Searcher:
    def __init__(self):
        pass

    @staticmethod
    def search_columns_data(index_name, source_names):
        # result = list(scan(es, index=index_name, doc_type=','.join(source_names),
        #                    query={"query": {"match_all": {}}}))
        result = list(data_collection.find({"set_name": index_name, "source_name": {"$in": source_names}}, {"_id": 0}))
        return result

    @staticmethod
    def search_column_data_by_name(column_name, index_name, source_name):
        result = data_collection.find_one(
            {"set_name": index_name, "source_name": source_name, "name": column_name, "value_list": {"$exists": True}},
            {"_id": 0})
        return result

    @staticmethod
    def get_coocurence_map(index_name, labeled_sources):
        matrix_dict = defaultdict(lambda: defaultdict(lambda: 0))
        result = list(coop_collection.find({"set_name": index_name, "source_name": {"$in": labeled_sources}}))
        for res in result:
            matrix_dict[res["type1"]][res["type2"]] += 1
        for key1 in matrix_dict.keys():
            for key2 in matrix_dict[key1].keys():
                matrix_dict[key1][key2] = matrix_dict[key1][key2] * 1.0 / len(labeled_sources)
            matrix_dict[key1][key1] = 1
        df = pd.DataFrame(matrix_dict).T.fillna(0)
        return df

    @staticmethod
    def search_relations_data(type1, type2, relation):
        result = relation_collection.find_one({"type1": type1, "type2": type2, "relation": relation}, {"_id": 0})
        return result

    @staticmethod
    def get_relation_score(type1, type2, relation):
        result = Searcher.search_relations_data(type1, type2, relation)
        if result:
            score = result["true_count"] * 1.0 / result["total_count"]
            print result["true_count"], result["total_count"], score
            return score
        return 0

    @staticmethod
    def search_similar_text_data(index_name, text, source_names):
        try:
            result = es.search(index=index_name, doc_type=','.join(source_names),
                               body={
                                   "query": {
                                       "match": {
                                           TF_TEXT: text,
                                       }
                                   }
                               },
                               size=10)
        except Exception as e:
            print e
            result = {"hits": {"hits": []}}
        return result

    @staticmethod
    def search_types_data(index_name, source_names):
        return Searcher.search_columns_data(index_name, source_names)
