from googletrans import Translator
from text_helpers import *
from cosine_sim import *
from operator import itemgetter
import requests
from bs4 import BeautifulSoup

def translate_operate_retrieve(original_query, k, e, dataset_hindi, dataset_english, N_hindi, N_english, total_vocab_hindi, total_vocab_english, total_vocab_size_hindi, total_vocab_size_english, DF_hindi, DF_english, D_hindi, D_english):
    translator = Translator()
    original_lang = translator.detect(original_query).lang
    translated_lang = ''
    translated_query = ''
    boost_multiplier = 1.5
    eng_queries = []
    hin_queries = []

    #Translate and Separate out to be boosted words
    if original_lang == 'en':
        translated_lang = 'hi'
        translated_query = translator.translate(original_query, dest='hi').text
        eng_queries = separate_boosted(original_query)
        hin_queries = separate_boosted(translated_query)

    else:
        original_lang = 'hi'
        translated_lang = 'en'
        translated_query = translator.translate(original_query, dest='en').text
        eng_queries = separate_boosted(translated_query)
        hin_queries = separate_boosted(original_query)

    #Array of index of articles and its corresponding cosine similarity values
    Q_cos_hin = []
    Q_cos_eng = []

    #Retrieving articles for original query
    #No query expansion call made
    if e==0:
        Q_hindi_first, cos_hindi_first  = cosine_similarity_hindi(k, hin_queries[0], N_hindi, total_vocab_size_hindi, total_vocab_hindi, DF_hindi, D_hindi)
        Q_english_first, cos_english_first  = cosine_similarity_english(k, eng_queries[0], N_english, total_vocab_size_english, total_vocab_english, DF_english, D_english)

        for i in range(len(Q_hindi_first)):
            Q_cos_hin.append((Q_hindi_first[i], cos_hindi_first[i]))

        for i in range(len(Q_english_first)):
            Q_cos_eng.append((Q_english_first[i], cos_english_first[i]))

        if len(hin_queries) > 1:
            #Retrieving Articles for boosted queries and boosting the similarity values
            for cur_query in hin_queries[1:]:
                Q_hindi, cos_hindi  = cosine_similarity_hindi(k, cur_query, N_hindi, total_vocab_size_hindi, total_vocab_hindi, DF_hindi, D_hindi)
                for i in range(len(Q_hindi)):
                    Q_cos_hin.append((Q_hindi[i], cos_hindi[i]*boost_multiplier))

            for cur_query in eng_queries[1:]:
                Q_english, cos_english  = cosine_similarity_english(k, cur_query, N_english, total_vocab_size_english, total_vocab_english, DF_english, D_english)
                for i in range(len(Q_english)):
                    Q_cos_eng.append((Q_english[i], cos_english[i]*boost_multiplier))


    #If Query expansion is true then expand
    if e==1:
        first_hin_expanded = hin_query_expand(hin_queries[0])
        first_eng_expanded = eng_query_expand(eng_queries[0])

        for cur_query in first_hin_expanded:
            Q_hindi, cos_hindi  = cosine_similarity_hindi(k, cur_query, N_hindi, total_vocab_size_hindi, total_vocab_hindi, DF_hindi, D_hindi)
            for i in range(len(Q_hindi)):
                Q_cos_hin.append((Q_hindi[i], cos_hindi[i]))

        for cur_query in first_eng_expanded:
            Q_english, cos_english  = cosine_similarity_english(k, cur_query, N_english, total_vocab_size_english, total_vocab_english, DF_english, D_english)
            for i in range(len(Q_english)):
                Q_cos_eng.append((Q_english[i], cos_english[i]))

        if len(hin_queries) > 1:
            #Retrieving Articles for boosted queries and boosting the similarity values
            for boosted_query in hin_queries[1:]:
                boost_hin_expanded = hin_query_expand(boosted_query)
                for cur_query in boost_hin_expanded:
                    Q_hindi, cos_hindi  = cosine_similarity_hindi(k, cur_query, N_hindi, total_vocab_size_hindi, total_vocab_hindi, DF_hindi, D_hindi)
                    for i in range(len(Q_hindi)):
                        Q_cos_hin.append((Q_hindi[i], cos_hindi[i]*boost_multiplier))

            for boosted_query in eng_queries[1:]:
                boost_eng_expanded = eng_query_expand(boosted_query)
                for cur_query in first_eng_expanded:
                    Q_english, cos_english  = cosine_similarity_english(k, cur_query, N_english, total_vocab_size_english, total_vocab_english, DF_english, D_english)
                    for i in range(len(Q_english)):
                        Q_cos_eng.append((Q_english[i], cos_english[i]*boost_multiplier))

    #Sorting and extracting Top 10 results
    Q_cos_eng_sorted = sorted(Q_cos_eng,key=itemgetter(1), reverse=True)
    Q_cos_hin_sorted = sorted(Q_cos_hin,key=itemgetter(1), reverse=True)

    top_k_hin = retrieve_top_k(Q_cos_hin_sorted, k, "hin")
    top_k_eng = retrieve_top_k(Q_cos_eng_sorted, k, "eng")

    make_output(original_lang, translated_lang, original_query, translated_query, top_k_hin, top_k_eng, dataset_hindi, dataset_english, k)
    return

def separate_boosted(query):
    boosted = re.findall("\[\[(.*?)\]\]", query)
    orig_query = re.sub("\[\[", "", query)
    orig_query = re.sub("\]\]", "", orig_query)
    all_queries = []
    all_queries.append(orig_query)
    all_queries.extend(boosted)
    return all_queries

def retrieve_top_k(cos_sorted, k, lang):
    top = []
    top_q = []
    for pair in cos_sorted:
        if len(top) == k:
            break
        if pair[0] not in top:
             top.append(pair[0])
             top_q.append(pair[1])

    sim_index_pair = []
    for i in range(0,len(top)):
        sim_index_pair.append([top[i], top_q[i], lang])
    return sim_index_pair

def hin_query_expand(query):
    preprocessed_query = preprocess_hin(query)
    tokens = word_tokenize(str(preprocessed_query))
    syn_dict = {}
    for token in tokens:
        with open('../Data/Synonyms/hindi_synonyms.txt') as openfileobject:
            for line in openfileobject:
                my_string = line
                my_string = re.sub("\t", " ", my_string)
                my_string = re.sub("-", " ", my_string)
                my_string = re.sub(",", " ",my_string)
                my_string = re.sub("।", " ", my_string)
                if token in my_string.split():
                    syn_dict[token] = my_string.split()
                    break

    expanded_queries = []

    for key in syn_dict.keys():
        syn_list = syn_dict[key]
        for syn in syn_list:
            expanded_queries.append(re.sub(key, syn, preprocessed_query))

    if not expanded_queries:
        expanded_queries.append(preprocessed_query)

    return expanded_queries

def eng_synonyms(term):
    response = requests.get('http://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, features = 'lxml')
    try:
        section = soup.find('section', {'class': 'synonyms-container'})
        return [span.text for span in section.findAll('span')]
    except:
        return []

def eng_query_expand(query):
    preprocessed_query = preprocess_eng(query)
    tokens = word_tokenize(str(preprocessed_query))

    syn_dict = {}
    for token in tokens:
        syn_list = eng_synonyms(token)
        if syn_list:
            syn_dict[token] = syn_list[:5]

    expanded_queries = []

    for key in syn_dict.keys():
        syn_list = syn_dict[key]
        for syn in syn_list:
            expanded_queries.append(re.sub(key, syn, preprocessed_query))

    if not expanded_queries:
        expanded_queries.append(preprocessed_query)

    return expanded_queries
