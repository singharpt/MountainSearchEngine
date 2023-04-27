import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Rocchio:
    """ 
    Rocchio Algorithm
    """
    def __init__(self, alpha=0.9, beta=0.3, gamma=0):
        # Alpha Value: Multiplying factor for query vector.
        self.alpha = alpha
        # Beta Value: Multiplying factor for relavant document vectors.
        self.beta = beta
        # Gamma Value: Multiplying factor for non-relavant document vectors.
        self.gamma = gamma
        
    # def get_top_K_relevant_documents(self, document_scores : list):
        """
        Parameters
        ---------------
        document_scores: list
            The vector of document scores computed before Rocchio's algorithm: [[doc_id, score][doc_id, score].......]
        
        Returns
        --------------
        Returns list of top K documents with highest scores
        """

        # return sorted(document_scores, reverse = True, key = lambda x: x[1])[:self.K]
    
    def get_centroid_of_relevant_vectors(self, query_vector, document_matrix):
        """
        Parameters
        ---------------
        document_matrix: list
            [[doc vector1], ......, [doc vector K]]      
        
        Returns
        --------------
        Returns numpy array of sum of all relevant documents divided by the count of relavant docuemnts
        """
        document_matrix = np.array(document_matrix)
        # print(document_matrix)
        # print(document_matrix.shape)
        row_l, column_l = document_matrix.shape
        # document_vector_size = len(document_matrix[0]) # check
        np_result_document_vector = np.zeros(query_vector.shape, dtype= float) # check datatype

        for np_document_vector in document_matrix:
            # np_document_vector = np.array(document_vector)
            np_doc = np.array(np_document_vector)
            np_result_document_vector = np.add(np_result_document_vector,np_doc)
        np_result_document_vector_divide_by_K = np_result_document_vector / row_l

        # print(f"Doc vector shape: {np_result_document_vector_divide_by_K.shape}")
        return np_result_document_vector_divide_by_K
    
    def get_document_matrix(self, document_ids, x):
        result = [] # change

        for id in document_ids:
            result.append(x[id].toarray().flatten())
            # result[id] = x[id].toarray().flatten()
            # print(result[id])

        # return result.values()
        return result
    
    def get_optimal_query_vector_using_rocchi_algorithm(self, query_vector, document_ids, tfidf_matrix):
        
        # np_query_vector = np.array(query_vector) # translate query vector to numpy
        # print(f"Input document_ids: {document_ids}")
        np_query_vector = query_vector.toarray()
        np_query_vector_alpha_factor = np_query_vector * self.alpha
        document_matrix = self.get_document_matrix(document_ids, tfidf_matrix)
        np_document_centroid_vector = self.get_centroid_of_relevant_vectors(np_query_vector_alpha_factor, document_matrix)
        np_document_centroid_vector_beta_factor = np_document_centroid_vector * self.beta
        
        # print("&&&&&&")
        # print(np_query_vector_alpha_factor.shape)
        # print(np_document_centroid_vector_beta_factor.shape)

        # print("&&&&&&&&")
        # print(type(np_query_vector_alpha_factor))
        # print(type(np_document_centroid_vector_beta_factor))
        np_optimal_query_vector = np.add(np_query_vector_alpha_factor,np_document_centroid_vector_beta_factor) # Not subtracting non-relevent doc as gamma = 0

        optimal_query_vector = np_optimal_query_vector

        cosinesimi = cosine_similarity(optimal_query_vector, tfidf_matrix).flatten()

        count = 0
        list_output_docs = []
        for score_rev in sorted(cosinesimi,reverse=True):
            if count == 5:
                break
            list_output_docs.append(np.where(cosinesimi==score_rev)[0][0])
            count+=1
        
        return list_output_docs

rocchio = Rocchio()
query_doc_vec = 1
list_output_docs = 1
x_loaded = 1
results = rocchio.et_optimal_query_vector_using_rocchi_algorithm(query_doc_vec, list_output_docs,x_loaded)