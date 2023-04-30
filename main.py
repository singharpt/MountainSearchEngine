import math
from flask import Flask, render_template, url_for, request
import bingquery as bing_call
import googlequery as google_call
from getSolrData import get_results_from_solr
from queryExpansion_association import *
# from getSolrData import *
import getSolrData
import clustering
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

        if btn == "Vector Space Relevance":
            qry = open("query.txt", "w")
            qry.write(inner_data)
            qry.close()
            print("Button pressed: Vector Space Relevance")

            qry_param = "text:(+%s)" % (inner_data)
            solr_results = getSolrData.get_results_from_solr(qry_param, 10)
            result = getSolrData.parse_solr_results(solr_results)
            
            Relevance_Results = result
            # Relevance_Results = "Button pressed: Vector Space Relevance"
            Query_Results = Google_Bing_Results(inner_data)
            # Relevance_Results = ["relevance_results('query.txt')"]

            qry = open("query.txt", "w")
            qry.write(inner_data)
            qry.close()
            qry_param = "text:(+%s)" % (inner_data)
            solr_results = getSolrData.get_results_from_solr(qry_param, 10)
            result = getSolrData.parse_solr_results(solr_results)
            btn = "Single-link Agglomerative Clustering"
            # Relevance_Results = clustering.get_clustering_results(result, btn)
            Cluster_Results = clustering.get_clustering_results(result, btn)
            # Relevance_Results, Cluster_Results = cluster_results('query.txt')
            # Relevance_Results = ['Test1']
            print("Cluster_Results: ", Cluster_Results)

            Query_Results = Google_Bing_Results(inner_data)
            print("Button pressed: Flat Clustering")


        if btn == "HITS":
            qry = open("query.txt", "w")
            qry.write(inner_data)
            qry.close()
            # Relevance_Results = relevance_results('query.txt')
            Query_Results = Google_Bing_Results(inner_data)
            Relevance_Results = ["relevance_results('query.txt')"]
            print("Button pressed: PageRanking + HITS")

        if btn == "PageRanking":
            qry = open("query.txt", "w")
            qry.write(inner_data)
            qry.close()
            # Relevance_Results = relevance_results('query.txt')
            Query_Results = Google_Bing_Results(inner_data)
            Relevance_Results = ["relevance_results('query.txt')"]
            print("Button pressed: PageRanking + HITS")

        if btn == "Flat Clustering":
            print("Button pressed: Flat Clustering ")
            qry = open("query.txt", "w")
            qry.write(inner_data)
            qry.close()
            qry_param = "text:(+%s)" % (inner_data)
            solr_results = getSolrData.get_results_from_solr(qry_param, 10)
            result = getSolrData.parse_solr_results(solr_results)

            # Relevance_Results = clustering.get_clustering_results(result, btn)
            Cluster_Results = clustering.get_clustering_results(result, btn)
            # Relevance_Results, Cluster_Results = cluster_results('query.txt')
            # Relevance_Results = ['Test1']
            print("Cluster_Results: ", Cluster_Results)
            
            Query_Results = Google_Bing_Results(inner_data)
            print("Button pressed: Flat Clustering")

        if btn == "Single-link Agglomerative Clustering":
            qry = open("query.txt", "w")
            qry.write(inner_data)
            qry.close()
            # Relevance_Results, Cluster_Results = cluster_results('query.txt')
            qry_param = "text:(+%s)" % (inner_data)
            solr_results = getSolrData.get_results_from_solr(qry_param, 10)
            result = getSolrData.parse_solr_results(solr_results)

            # Relevance_Results = clustering.get_clustering_results(result, btn)
            Cluster_Results = clustering.get_clustering_results(result, btn)
            Query_Results = Google_Bing_Results(inner_data)
            print("Button pressed: Agglomerative Clustering")
            print("Cluster_Results: ", Cluster_Results)
        
        if btn == "Complete-link Agglomerative Clustering":
            qry = open("query.txt", "w")
            qry.write(inner_data)
            qry.close()
            # Relevance_Results, Cluster_Results = cluster_results('query.txt')
            qry_param = "text:(+%s)" % (inner_data)
            solr_results = getSolrData.get_results_from_solr(qry_param, 10)
            result = getSolrData.parse_solr_results(solr_results)

            Relevance_Results = clustering.get_clustering_results(result, btn)
            # Cluster_Results = clustering.get_clustering_results(result, btn)
            Query_Results = Google_Bing_Results(inner_data)
            print("Button pressed: Agglomerative Clustering")

        if btn == "Association Clustering":
            solr_query_format = "content:({})".format(inner_data)
            solr_results = get_results_from_solr(solr_query_format, 50)
            documents = get_documents(solr_results)
            expanded_query = association_main(inner_data, documents)

        if btn == "Scalar Clustering":
            pass

        if btn == "Metric Clustering":
            pass

        if btn == "Query Expansion Rocchio":
            pass

        if btn == "Rocchio Algorithm":
            pass

        if btn == 'reset':
            pass
            # Query_Results = False
            # Relevance_Results = False
            # Cluster_Results = False
            # Query_Expansion_Results = False

    return render_template('ir.html', Query_Results=Query_Results, Relevance_Results=Relevance_Results, Cluster_Results=False)


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

