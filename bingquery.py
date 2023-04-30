# subscription_key = "f5fd22bb93334ca9a4d4208040ce9031"
# assert subscription_key
#
# search_url = "https://api.bing.microsoft.com/v7.0/search"
# search_term = "Mountains"

# import requests
#
# headers = {"Ocp-Apim-Subscription-Key": subscription_key}
# params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
# response = requests.get(search_url, headers=headers, params=params)
# response.raise_for_status()
# search_results = response.json()
#
# print(search_results)


# ********************


import imp
from itertools import count
import requests
import json
from pprint import pprint
from IPython.display import HTML
import re

subscription_key = "f5fd22bb93334ca9a4d4208040ce9031"
assert subscription_key
search_url = "https://api.bing.microsoft.com/v7.0/search?responseFilter=webpages"
# search_term = "The University of Texas at Dallas"

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
remove_tags = re.compile('<.*?>')

def b_search(search_term):
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML", "count" : 10}
    response = requests.get(search_url, headers=headers, params=params)
    # print("\nHeaders:\n")
    # print(response.headers)
    # print(type(response))
    # res_obj = json.loads(response)
    # print("\nJSON Response:\n")
    results = response.json()["webPages"]
    final_result_values = results['value']
    # pprint(response.json()["webPages"])
    b_res = []
    for result in final_result_values:
        # print(type(result))
        # print(result['url'])
        # for key, value in result.items():
        #     print(key, value)
        link = result['url']
        # snippet = result['snippet']
        # displayLink = result['displayUrl']

        # link =  re.sub(remove_tags, '', result['url'])
        snippet =re.sub(remove_tags, '', result['snippet'])
        displayLink = re.sub('https://', '', re.sub(remove_tags, '',result['displayUrl']))

        temp_list_one_q = [link, displayLink, snippet]
        print(temp_list_one_q)
        b_res.append(temp_list_one_q)
    # print(b_res)
    return b_res
# st = "The University of Texas at Dallas"
# b_search("The University of Texas at Dallas")