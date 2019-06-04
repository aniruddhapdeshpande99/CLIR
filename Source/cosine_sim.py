from text_helpers import *

def calc_DF(dataset):
    DF = {}

    for i in dataset.keys():
        tokens = dataset[i]['processed_text']
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}

        tokens = dataset[i]['processed_title']
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}
    for i in DF:
        DF[i] = len(DF[i])

    return DF

def doc_freq(word, DF):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c


def calc_tf_idf(dataset, N, DF):
    alpha = 0.3

    tf_idf = {}

    for i in dataset.keys():

        tokens = dataset[i]['processed_text']

        counter = Counter(tokens + dataset[i]['processed_title'])
        words_count = len(tokens + dataset[i]['processed_title'])

        for token in np.unique(tokens):

            tf = counter[token]/words_count
            df = doc_freq(token, DF)
            idf = np.log((N+1)/(df+1))

            tf_idf[dataset[i]['index'], token] = tf*idf

    tf_idf_title = {}

    for i in dataset.keys():

        tokens = dataset[i]['processed_title']
        counter = Counter(tokens + dataset[i]['processed_text'])
        words_count = len(tokens + dataset[i]['processed_text'])

        for token in np.unique(tokens):

            tf = counter[token]/words_count
            df = doc_freq(token, DF)
            idf = np.log((N+1)/(df+1)) #numerator is added 1 to avoid negative values

            tf_idf_title[dataset[i]['index'], token] = tf*idf

    for i in tf_idf:
        tf_idf[i] *= alpha

    for i in tf_idf_title:
        tf_idf[i] = tf_idf_title[i]

    return tf_idf


def vectorise_tf_idf(N, total_vocab_size, total_vocab, tf_idf):
    D = np.zeros((N, total_vocab_size))
    for i in tf_idf:
        try:
            ind = total_vocab.index(i[1])
            D[i[0]][ind] = tf_idf[i]
        except:
            pass
    return D

def gen_vector(tokens, N, total_vocab_size, total_vocab, DF):

    Q = np.zeros((len(total_vocab)))

    counter = Counter(tokens)
    words_count = len(tokens)

    query_weights = {}

    for token in np.unique(tokens):

        tf = counter[token]/words_count
        df = doc_freq(token, DF)
        idf = math.log((N+1)/(df+1))

        try:
            ind = total_vocab.index(token)
            Q[ind] = tf*idf
        except:
            pass
    return Q

def cosine_sim(a, b):
    if np.linalg.norm(a)*np.linalg.norm(b) != 0.0:
        cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    else:
         cos_sim = 0.0
    return cos_sim

def cosine_similarity_hindi(k, query, N_hindi, total_vocab_size_hindi, total_vocab_hindi, DF_hindi, D_hindi):
    preprocessed_query = preprocess_hin(query)
    tokens = word_tokenize(str(preprocessed_query))
    d_cosines = []

    query_vector = gen_vector(tokens, N_hindi, total_vocab_size_hindi, total_vocab_hindi, DF_hindi)

    for d in D_hindi:
        d_cosines.append(cosine_sim(query_vector, d))

    out = np.array(d_cosines).argsort()[-k:][::-1]

    sorted_cos = []

    for i in out:
        sorted_cos.append(d_cosines[i])

    return out, sorted_cos

def cosine_similarity_english(k, query, N_english, total_vocab_size_english, total_vocab_english, DF_english, D_english):
    preprocessed_query = preprocess_eng(query)
    tokens = word_tokenize(str(preprocessed_query))
    d_cosines = []

    query_vector = gen_vector(tokens, N_english, total_vocab_size_english, total_vocab_english, DF_english)

    for d in D_english:
        d_cosines.append(cosine_sim(query_vector, d))

    out = np.array(d_cosines).argsort()[-k:][::-1]

    sorted_cos = []

    for i in out:
        sorted_cos.append(d_cosines[i])

    return out, sorted_cos
