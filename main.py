from flask import Flask, render_template, request
import bingquery as bing_call
import googlequery as google_call
from queryExpansion_association import *
from queryExpansion_scalar import *
from queryExpansion_metric import *
from queryExpansion_rocchio import *
from pageRank import *
from getSolrData import *
from hitsScore import *
from clustering import *
import json

title_link_dict = {}

app = Flask(__name__)
QR = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    Query_Results = False
    Relevance_Results = False
    Cluster_Results = False
    Query_Expansion_Results = False
    HITS = False
    PageRanking = False
    Search_Results = False
    Query = ""
    expanded_query = ""
    if request.method == 'POST':
        data = json.dumps(dict(request.form))
        print(data)
        print(type(data))
        form_data = json.loads(data)
        # print(data)
        inner_data = form_data['query']
        Query = inner_data
        btn = [form_data['relevance'], form_data['clustering'], form_data['expansion']]
        btn = [s for s in btn if s != ""]
        if len(btn) > 0:
            btn = btn[0]
        else:
            btn = 'reset'
        qry = open("query.txt", "w")
        print("btn: ", btn)

        if len(inner_data) > 0:

            solr_query_format = "content:(+{})".format(inner_data)
            # Query_Results = Google_Bing_Results(inner_data)

            if btn == "Vector Space Relevance":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                print("Button pressed: Vector Space Relevance")
                solr_results = get_results_from_solr(solr_query_format, 20)
                Relevance_Results = parse_solr_results(solr_results)

            if btn == "HITS":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                solr_results = get_results_from_solr(solr_query_format, 20)
                solr_results = parse_solr_results(solr_results)
                authority_score_dict = get_authority_scores_data()
                Relevance_Results = add_authority_scores(solr_results, authority_score_dict)
                print(Relevance_Results)

            if btn == "PageRanking":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                solr_results = get_results_from_solr(solr_query_format, 20)
                solr_results = parse_solr_results(solr_results)
                pagerank_score_dict = get_pagerank_scores_data()
                Relevance_Results = add_pagerank_scores(solr_results, pagerank_score_dict)
                print(Relevance_Results)
                
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
                solr_results = get_results_from_solr(solr_query_format, 10)
                documents = get_documents(solr_results)
                expanded_query = association_main(inner_data, documents)
                print("Expanded Query : ", expanded_query)
                new_solr_results = get_results_from_solr("content:({})".format(expanded_query), 20)
                Query_Expansion_Results = parse_solr_results(new_solr_results)

            if btn == "Scalar Clustering":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                solr_results = get_results_from_solr(solr_query_format, 20)
                documents = get_documents(solr_results)
                expanded_query = scalar_main(inner_data, documents)
                print("Expanded Query : ", expanded_query)
                solr_results = get_results_from_solr("content:({})".format(expanded_query), 20)
                Query_Expansion_Results = parse_solr_results(solr_results)

            if btn == "Metric Clustering":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                solr_results = get_results_from_solr(solr_query_format, 20)
                documents = get_documents(solr_results)
                expanded_query = metric_main(inner_data, documents)
                print("Expanded Query : ", expanded_query)
                solr_results = get_results_from_solr("content:({})".format(expanded_query), 20)
                Query_Expansion_Results = parse_solr_results(solr_results)

            if btn == "Rocchio Algorithm":
                print("Button pressed: ", btn)
                print('Query entered: ', inner_data)
                rocchio = Rocchio(inner_data)
                expanded_query = rocchio.rocchio_main()
                print("Expanded Query : ", expanded_query)
                solr_results = get_results_from_solr("content:({})".format(expanded_query), 20)
                Query_Expansion_Results = parse_solr_results(solr_results)

            if btn == 'Reset':
                Query_Results = False
                Relevance_Results = False
                Cluster_Results = False
                Query_Expansion_Results = False
                Query=False
                expanded_query = ""

    return render_template('ir.html', Expanded_Query=expanded_query, Query=Query, Query_Results=Query_Results, Relevance_Results=Relevance_Results, Query_Expansion_Results=Query_Expansion_Results, Cluster_Results=Cluster_Results)
# pull everything to main
# go to userinterface and merge

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
    b_results = bing_call.b_search(search_query)
    query_result_dict['google'] = g_results
    query_result_dict['bing'] = b_results

    return query_result_dict

# def relevance_results(query_file):
#     r_results = []
#     results = relevance.Indexing(query_file)
#     # print(results)
#     # for doc in results:
#     #   temp_list = [title_link_dict[doc][0], title_link_dict[doc][1]]
#     #   r_results.append(temp_list)
#     r_results = get_title_link(results)
#     # print(r_results)
#     return r_results
#
#
# def cluster_results(query_file):
#     c_results = {}
#     c_results_list = []
#     r_results = []
#     results = relevance.Indexing(query_file)
#     r_results = get_title_link(results)
#     c_results = cr.fetch_topm_docs(results)
#     for key, value in c_results.items():
#         c_results_list.append(get_title_link(value))
#
#     # for doc in results:
#     #   temp_list = [title_link_dict[doc][0], title_link_dict[doc][1]]
#     #   r_results.append(temp_list)
#     print(results)
#     print(r_results)
#     print(c_results)
#
#     return r_results, c_results_list


# relevance_results('query.txt')
# cluster_results('query.txt')

if __name__ == "__main__":
    app.run(debug=True)

