from getSolrData import get_results_from_solr, parse_solr_results
import json
pagerank_score_file = "pagerank_scores"

def get_pagerank_scores_data():
    f = open(pagerank_score_file, "r")
    string_dict = f.readline()
    pagerank_score_dict = json.loads(string_dict)
    return pagerank_score_dict

def add_pagerank_scores(solr_results, pagerank_score_dict):
    for res in solr_results:
        if res['url'].strip() in pagerank_score_dict:
            res['pagerank_score'] = float(pagerank_score_dict[res['url']])
        else:
            res['pagerank_score'] = 0
    solr_results = sorted(solr_results, key=lambda x:x['pagerank_score'], reverse=True)
    return solr_results

# query = "content:(mountains)"
# solr_results = get_results_from_solr(query, 10)
# solr_results = parse_solr_results(solr_results)
# pagerank_score_dict = get_pagerank_scores_data()
# new_solr_results = add_pagerank_scores(solr_results, pagerank_score_dict)

# for x in new_solr_results:
#     print(x['pagerank_score'], "\n")

# get_documents(solr_results)