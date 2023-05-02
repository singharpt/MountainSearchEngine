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

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
remove_tags = re.compile('<.*?>')

def b_search(search_term):
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML", "count" : 10}
    response = requests.get(search_url, headers=headers, params=params)

    results = response.json()["webPages"]
    final_result_values = results['value']

    b_res = []
    for result in final_result_values:

        link = result['url']
        snippet =re.sub(remove_tags, '', result['snippet'])
        displayLink = re.sub('https://', '', re.sub(remove_tags, '',result['displayUrl']))

        temp_list_one_q = [link, displayLink, snippet]
        print(temp_list_one_q)
        b_res.append(temp_list_one_q)
    return b_res
