import math
from flask import Flask, render_template, url_for, request
import bingquery as bing_call
import googlequery as google_call
from queryExpansion_association import *
from pageRank import *
from getSolrData import *
from hitsScore import *
import getSolrData
from clustering import *
# from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# import math
# from sklearn.metrics.pairwise import cosine_similarity
# import os
# import pickle
# import time
# import numpy as np
# from scipy import sparse
# from sknetwork.ranking import PageRank
# import pandas as pd
import json


# import ast
# from bs4 import BeautifulSoup

# import Finally_Sunday as relevance
# import cluster_k as cr

title_link_dict = {}
# with open('result_final.json') as json_file:
#     title_link_dict = json.load(json_file)

app = Flask(__name__)
QR = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    rel_docs = False
    Query_Results = False
    Relevance_Results = False
    Cluster_Results = False
    Query_Expansion_Results = False
    HITS = False
    PageRanking = False
    Search_Results = False

    if request.method == 'POST':
        data = json.dumps(dict(request.form))
        print(data)
        print(type(data))
        form_data = json.loads(data)
        # print(data)
        inner_data = form_data['query']
        btn = [form_data['relevance'], form_data['clustering'], form_data['expansion']]
        btn = [s for s in btn if s != ""]
        if len(btn) > 0:
            btn = btn[0]
        else:
            btn = 'reset'
        qry = open("query.txt", "w")
        print("btn: ", btn)

        if len(inner_data) > 0:

            solr_query_format = "content:({})".format(inner_data)
            # Query_Results = Google_Bing_Results(inner_data)

            if btn == "Vector Space Relevance":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                print("Button pressed: Vector Space Relevance")
                solr_results = get_results_from_solr(solr_query_format, 10)
                Relevance_Results = parse_solr_results(solr_results)

            if btn == "HITS":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                solr_results = get_results_from_solr(solr_query_format, 10)
                solr_results = parse_solr_results(solr_results)
                authority_score_dict = get_authority_scores_data()
                Relevance_Results = add_authority_scores(solr_results, authority_score_dict)

            if btn == "PageRanking":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                solr_results = get_results_from_solr(inner_data, 10)
                solr_results = parse_solr_results(solr_results)
                pagerank_score_dict = get_pagerank_scores_data()
                Relevance_Results = add_pagerank_scores(solr_results, pagerank_score_dict)
                
            if btn == "Flat Clustering":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                solr_results = get_results_from_solr(solr_query_format, 10)
                parse_results = parse_solr_results(solr_results)
                Cluster_Results = get_clustering_results(parse_results, btn)
                print(Cluster_Results)

            if btn == "Single-link Agglomerative Clustering":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                solr_results = get_results_from_solr(solr_query_format, 10)
                parse_results = parse_solr_results(solr_results)
                Cluster_Results = get_clustering_results(parse_results, btn)
                print(Cluster_Results)
                
            if btn == "Complete-link Agglomerative Clustering":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                solr_results = get_results_from_solr(solr_query_format, 10)
                parse_results = parse_solr_results(solr_results)
                Cluster_Results = get_clustering_results(parse_results, btn)
                print(Cluster_Results)

            if btn == "Association Clustering":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)

            if btn == "Scalar Clustering":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)

            if btn == "Metric Clustering":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)

            if btn == "Query Expansion Rocchio":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)

            if btn == "Rocchio Algorithm":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)

            if btn == 'reset':
                Query_Results = False
                Relevance_Results = False
                Cluster_Results = False
                Query_Expansion_Results = False

    return render_template('ir.html', Search_Results= Search_Results, Query_Results=Query_Results, Relevance_Results=Relevance_Results, Cluster_Results=Cluster_Results)


def get_title_link(results):
    res = []
    for doc in results:
        temp_list = [title_link_dict[doc][0], title_link_dict[doc][1]]
        res.append(temp_list)
    return res


def Google_Bing_Results(search_query):
    query_result_dict = {}
    g_results = []
    b_results = []
    g_results = google_call.g_search(search_query)
    # print(g_results)
    b_results = bing_call.b_search(search_query)
    # print("=================GOOGLE===================")
    # for i in range(len(g_results)):
    #     print(i+1)
    #     print("Link:", g_results[i][0])
    #     print("Display Link:", g_results[i][1])
    #     print("Snippet:", g_results[i][2])
    # print("=================BING===================")
    # for i in range(len(b_results)):
    #     print(i+1)
    #     print("Link:", b_results[i][0])
    #     print("Display Link:", b_results[i][1])
    #     print("Snippet:", b_results[i][2])
    query_result_dict['google'] = g_results
    query_result_dict['bing'] = b_results

    return query_result_dict


# st ='The University of Texas at Dallas'
# q_dict = Google_Bing_Results(st)


# for i in range(len(q_dict['google'])):
#     print("=================GOOGLE===================")
#     print(i+1)
#     print("Link:", q_dict['google'][i][0])
#     print("Display Link:", q_dict['google'][i][1])
#     print("Snippet:", q_dict['google'][i][2])
#     print("=================BING===================")
#     print(i+1)
#     print("Link:", q_dict['bing'][i][0])
#     print("Display Link:", q_dict['bing'][i][1])
#     print("Snippet:", q_dict['bing'][i][2])

def relevance_results(query_file):
    r_results = []
    results = relevance.Indexing(query_file)
    # print(results)
    # for doc in results:
    #   temp_list = [title_link_dict[doc][0], title_link_dict[doc][1]]
    #   r_results.append(temp_list)
    r_results = get_title_link(results)
    # print(r_results)
    return r_results


def cluster_results(query_file):
    c_results = {}
    c_results_list = []
    r_results = []
    results = relevance.Indexing(query_file)
    r_results = get_title_link(results)
    c_results = cr.fetch_topm_docs(results)
    for key, value in c_results.items():
        c_results_list.append(get_title_link(value))

    # for doc in results:
    #   temp_list = [title_link_dict[doc][0], title_link_dict[doc][1]]
    #   r_results.append(temp_list)
    print(results)
    print(r_results)
    print(c_results)

    return r_results, c_results_list


# relevance_results('query.txt')
# cluster_results('query.txt')

if __name__ == "__main__":
    app.run(debug=True)

