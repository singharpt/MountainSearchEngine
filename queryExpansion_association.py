from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from string import punctuation
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

def tokenize_doc(doc_text):
    words =  wordpunct_tokenize(doc_text.lower())
    stop_words = stopwords.words("english")
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    wordsFiltered = []
    for w in words:
        if w not in punctuation and w not in stop_words and not w.isnumeric():
            wordsFiltered.append(w)
    lemmas = [lemmatizer.lemmatize(token) for token in wordsFiltered]
    lemmas = list(set(lemmas))
    return lemmas

def build_association(id_token_map, vocab, query):
    association_list = []
    for i, voc in enumerate(vocab):
        for word in query:
            c1, c2, c3 = 0, 0, 0
            for doc_id, tokens_this_doc in id_token_map.items():
                count0 = tokens_this_doc.count(voc)
                count1 = tokens_this_doc.count(word)
                c1 += count0 * count1
                c2 += count0 * count0
                c3 += count1 * count1
            c1 /= (c1 + c2 + c3)
            if c1 != 0:
                association_list.append((voc, word, c1))
    return association_list

def association_main(query, solr_results):
    vocab = []
    tokens_map = {}
    query = tokenize_doc(query)

    for result in solr_results:
        tokens_this_document = tokenize_doc(result['content'])
        tokens_map[result['digest']] = tokens_this_document
        vocab.extend(tokens_this_document)

    vocab = set(vocab)
    association_list = build_association(tokens_map, vocab, query)
    association_list.sort(key = lambda x: x[2],reverse=True)

    i=1
    loop_limit = len(query) * 4
    print(loop_limit)
    expanded_query = []
    while(i<loop_limit):
        expanded_query.append(association_list[i][0])
        i +=1
    expanded_query.extend(query)
    return " ".join(set(expanded_query))

def get_documents(solr_results):
    documents = []
    for doc in solr_results:
        if "content" in doc:
            documents.append(doc)
    return documents
