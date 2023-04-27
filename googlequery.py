from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyDuJcLFgsxMKxUnuJTN1zw9Rv_H17cAs4w"
my_cse_id = "7568448c0fe934725"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def g_search(query):
    g_res = []
    results = results = google_search(
        query, my_api_key, my_cse_id, num=10)
    for result in results:
        link = ""
        snippet= ""
        displayLink =""
        link = result['formattedUrl']
        # print(result['snippet'])
        if "snippet" not in result.keys():
            snippet = ""
        else:
            snippet = result['snippet']
        # snippet = result['snippet']
        # print(snippet)
        # snippet = "X"
        displayLink = result['displayLink']
        temp_list_one_q = [link, displayLink, snippet]
        print("temp_list_one_q", temp_list_one_q)
        g_res.append(temp_list_one_q)


    return g_res
