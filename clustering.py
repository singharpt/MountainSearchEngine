from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram
import pandas as pd


def get_clustering_results(clust_inp, param_type, inner_data):
    # fetched_url = process_query(clust_inp, inner_data)
    global lines
    if param_type == "Flat Clustering":
        fetched_url = process_query(clust_inp, inner_data)
        f = open('clustering_data/flat_clustering.txt')
        lines = f.readlines()
        f.close()

    elif param_type == "Single-link Agglomerative Clustering":
        f = open('clustering_data/single_link_data.txt')
        lines = f.readlines()
        f.close()
    
    elif param_type == "Complete-link Agglomerative Clustering":
        f = open('clustering_data/complete_link_data.txt')
        lines = f.readlines()
        f.close()

    cluster_map = {}
    print("Length of lines is :", len(lines))
    for line in lines:
        line_split = line.split(",")
        if line_split[1] == "\n" or line_split[1] == "":
            line_split[1] = "31.0"
        elif(len(line_split) < 2):
            break
        cluster_map.update({line_split[0]: line_split[1]})

    

    for curr_resp in clust_inp:
        curr_url = curr_resp["url"]
        curr_cluster = cluster_map.get(curr_url, "31.0")
        curr_resp.update({"cluster": curr_cluster})
        curr_resp.update({"done": "False"})
        curr_resp.update({"first": "False"})

    clust_resp = []
    curr_rank = 1
    if param_type == "Flat Clustering":
        fetched_cluster = cluster_map[fetched_url]
        # if(fetched_cluster == "\n"):
            # fetched_cluster = "31.0"
        print("Fetched Cluster is",fetched_cluster)
        for curr_resp in clust_inp:
            # print("Current_resp cluster is", curr_resp["cluster"])
            if  curr_resp["done"] == "False" and curr_resp["cluster"] == fetched_cluster:
                clust = fetched_cluster
                curr_resp.update({"done": "True"})
                curr_resp.update({"rank": str(curr_rank)})
                curr_rank += 1
                clust_resp.append({"title": curr_resp["title"], "url": curr_resp["url"],
                                "meta_info": curr_resp["meta_info"], "rank": curr_resp["rank"], "cluster" : clust})
                for remaining_resp in clust_inp:
                    if remaining_resp["done"] == "False":
                        if remaining_resp["cluster"] == fetched_cluster:
                            remaining_resp.update({"done": "True"})
                            remaining_resp.update({"rank": str(curr_rank)})
                            curr_rank += 1
                            clust_resp.append({"title": remaining_resp["title"], "url": remaining_resp["url"],
                                            "meta_info": remaining_resp["meta_info"], "rank": remaining_resp["rank"], "cluster" : clust})

    for curr_resp in clust_inp:
        if curr_resp["done"] == "False":
            curr_cluster = curr_resp["cluster"]
            curr_resp.update({"done": "True"})
            curr_resp.update({"rank": str(curr_rank)})
            curr_rank += 1
            clust_resp.append({"title": curr_resp["title"], "url": curr_resp["url"],
                               "meta_info": curr_resp["meta_info"], "rank": curr_resp["rank"], "cluster" : curr_cluster})
            for remaining_resp in clust_inp:
                if remaining_resp["done"] == "False":
                    if remaining_resp["cluster"] == curr_cluster:
                        remaining_resp.update({"done": "True"})
                        remaining_resp.update({"rank": str(curr_rank)})
                        curr_rank += 1
                        clust_resp.append({"title": remaining_resp["title"], "url": remaining_resp["url"],
                                           "meta_info": remaining_resp["meta_info"], "rank": remaining_resp["rank"], "cluster" : curr_cluster})

    return clust_resp

def process_query(clust_inp, query):

    document_list = []
    url_list = []

    # Parse text content from indexed json
    for curr_resp in clust_inp:
        url_list.append(curr_resp["url"])
        document_list.append(curr_resp["meta_info"])
    print("Document list is of length", len(document_list))
    vectorizer = TfidfVectorizer(min_df=0.0, stop_words='english', use_idf=True)
    X = vectorizer.fit_transform(document_list)

    km = KMeans(n_clusters = 50, init='k-means++')
    km.fit(X)

    id_series = pd.Series(url_list)
    cluster_series = pd.Series(km.labels_)
    results = (pd.concat([id_series,cluster_series], axis=1))
    results.columns = ['id', 'cluster']
    # clean_query = preprocess(query)

    # vectorize the query using the same TfidfVectorizer object
    query_vector = vectorizer.transform([query])
    print(query_vector)
    # predict the cluster label for the vectorized query
    # query_cluster = km.predict(query_vector)[0]
    # print("Predicted query_cluster is:", query_cluster)
    # get the centroid vectors for each cluster
    centroid_vectors = km.cluster_centers_

    # compute the cosine similarity between the vectorized query and each centroid vector
    similarities = cosine_similarity(query_vector, centroid_vectors)
    # print("Length of similarities is:", similarities[0])
    # get the cluster with the highest similarity score
    closest_cluster = np.argmax(similarities)

    cluster_urls = results.loc[results['cluster'] == closest_cluster]
    url = cluster_urls['id'].iloc[0]
    print(url)
    print("The closest cluster to the query is:", closest_cluster)

    return url