from getSolrData import get_results_from_solr, parse_solr_results
import json
from collections import OrderedDict

hits_score_file = "hubs_score"
authority_score_file = "authority_score"


def get_authority_scores_data():
    f = open(authority_score_file, "r")
    string_dict = f.readline()
    authority_score_dict = json.loads(string_dict)
    return authority_score_dict

def add_authority_scores(solr_results, authority_score_dict):
    for res in solr_results:
        if res['url'] in authority_score_dict:
            res['authority_score'] = authority_score_dict[res['url']]
        else:
            res['authority_score'] = 0
    solr_results = sorted(solr_results, key=lambda x:x['authority_score'], reverse=True)
    return solr_results

query = "content:(mountains)"
solr_results = get_results_from_solr(query, 10)
solr_results = parse_solr_results(solr_results)
authority_score_dict = get_authority_scores_data()
new_solr_results = add_authority_scores(solr_results, authority_score_dict)

for x in new_solr_results:
    print(x['authority_score'], "\n")

# get_documents(solr_results)