import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from string import punctuation
from nltk import PorterStemmer
from tqdm import tqdm

porter_stemmer = PorterStemmer()

def tokenize_text(doc_text):
    stop_words = set(stopwords.words('english'))
    words =  wordpunct_tokenize(doc_text.lower())
    stop_words = stopwords.words("english")
    wordsFiltered = []
    for w in words:
        if w not in punctuation and w not in stop_words and not w.isnumeric():
            wordsFiltered.append(w)
    return wordsFiltered

def make_stem_map(vocab):
    """
    Args:
        vocab(list): a list of vocabulary
    Returns:
        token_2_stem(dict): a map from token to its stem having structure {token:stem}
        stem_2_tokens(dict): a map from stem to its corresponding tokens having structure:
                             {stem:set(token_1, token_2, ...)}
    """
    token_2_stem = {} # 1 to 1
    stem_2_tokens = {} # 1 to n

    for token in vocab:
        stem = porter_stemmer.stem(token)
        if stem not in stem_2_tokens:
            stem_2_tokens[stem] = set()
        stem_2_tokens[stem].add(token)
        token_2_stem[token] = stem

    return token_2_stem, stem_2_tokens 

def get_scalar_cluster(doc_tokens, token_2_stem, stem_2_tokens, query):
    """
    Args:
        doc_tokens(2-D list): tokens in each documents having structure:
                              [[token_1, token_2, ...], [...], ...]
        token_2_stem(dict): a map from token to its stem having structure {token:stem}
        stem_2_tokens(dict): a map from stem to its corresponding tokens having structure:
                             {stem:set(token_1, token_2, ...)}
        query(list): a list of tokens from query
        
    Return:
        query_expands(list): list of expand stem tokens ids for each token in the query
    """
    # build map from stem to index
    stems = stem_2_tokens.keys()
    stems = list(sorted(stems))
    stem_2_idx = {s:i for i, s in enumerate(stems)}

    # frequency of stems in each document
    f = np.zeros((len(doc_tokens), len(stems)), dtype=np.int32)
    for doc_id, tokens in enumerate(doc_tokens):
        for token in tokens:
            if token in token_2_stem:
                stem = token_2_stem[token]
                stem_idx = stem_2_idx[stem]
                f[doc_id, stem_idx] += 1

    # correlation matrix
    c = np.dot(f.T, f) # (#_of_stems, #_of_stems)
    c_diag = np.expand_dims(np.diag(c), axis=0) # extract all c_{u,u} shape: (1, #_of_stems)

    # normalize correlation matrix
    s = c / (c + c_diag + c_diag.T) # (#_of_stems, #_of_stems)
    s_norm = np.linalg.norm(s, axis=1) # (#_of_stems,)

    # expand query
    query_expands_id = []
    for token in query:
        stem_id = stem_2_idx[token]

        # calculate cosine simialrity for the token with all other stems
        stem_vec = np.expand_dims(s[stem_id, :], axis=0)
        stem_norm = np.linalg.norm(stem_vec)
        s_stem = np.dot(stem_vec, s.T).squeeze() # (#_of_stems,)
        s_stem = (s_stem / stem_norm) / s_norm # cosine similarity

        # pick the top 3 stems for each query token
        idx_sort = np.argsort(s_stem)[::-1] # sort decreasing by score
        idx_sort = idx_sort[:2]
        query_expands_id.extend(idx_sort.tolist())

    # convert stem ids to stem
    query_expands = []
    for stem_idx in query_expands_id:
        query_expands.append(stems[stem_idx])

    return query_expands

def scalar_main(query, solr_results):
    """
    Args:
        query(str): a text string of query
        solr_results(list): result for the query from function 'get_results_from_solr'
    Return:
        query(str): a text string of expanded query
    """
    vocab = set()
    doc_tokens = []

    # tokenize query and query results, then build vocabulary
    query = tokenize_text(query)
    query = [porter_stemmer.stem(token) for token in query] 

    vocab.update(query)
    for result in tqdm(solr_results, desc='Preprocessing results'):
        if 'content' not in result:
            tokens = []
        else:
            tokens = tokenize_text(result['content'])
        doc_tokens.append(tokens)
        vocab.update(tokens)

    vocab = list(sorted(vocab))
    token_2_stem, stem_2_tokens = make_stem_map(vocab)

    # expand query
    query_expands_stem = get_scalar_cluster(doc_tokens, token_2_stem, stem_2_tokens, query)

    query.extend(query_expands_stem) 
    query = ' '.join(list(set(query)))

    return query

def get_documents(solr_results):
    documents = []
    for doc in solr_results:
        if "content" in doc:
            documents.append(doc)
    return documents