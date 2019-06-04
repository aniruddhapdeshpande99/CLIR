from text_helpers import *
from cosine_sim import *
from query_operations import *
import argparse
import webbrowser

def main():
    #Reading and Preparing Data
    dataset_english = read_data_eng()
    dataset_hindi = read_data_hin()
    N_english = len(dataset_english)
    N_hindi = len(dataset_hindi)

    for i in dataset_english.keys():
        dataset_english[i]['processed_text'] = word_tokenize(str(preprocess_eng(dataset_english[i]['text'])))
        dataset_english[i]['processed_title'] = word_tokenize(str(preprocess_eng(dataset_english[i]['title'])))

    for i in dataset_hindi.keys():
        dataset_hindi[i]['processed_text'] = word_tokenize(str(preprocess_hin(dataset_hindi[i]['text'])))
        dataset_hindi[i]['processed_title'] = word_tokenize(str(preprocess_hin(dataset_hindi[i]['title'])))

    DF_english = calc_DF(dataset_english)
    DF_hindi = calc_DF(dataset_hindi)

    total_vocab_size_english = len(DF_english)
    total_vocab_english = [x for x in DF_english]

    total_vocab_size_hindi = len(DF_hindi)
    total_vocab_hindi = [x for x in DF_hindi]

    tf_idf_english = calc_tf_idf(dataset_english, N_english, DF_english)
    tf_idf_hindi = calc_tf_idf(dataset_hindi, N_hindi, DF_hindi)

    D_english = vectorise_tf_idf(N_english, total_vocab_size_english, total_vocab_english, tf_idf_english)
    D_hindi = vectorise_tf_idf(N_hindi, total_vocab_size_hindi, total_vocab_hindi, tf_idf_hindi)

    #Reading Query from Command Line
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("k")
    parser.add_argument("e")
    args = parser.parse_args()
    k = int(args.k)
    e = int(args.e)
    original_query = args.query

    #Setting up translator and translating query from L1 to L2
    translate_operate_retrieve(original_query, k, e, dataset_hindi, dataset_english, N_hindi, N_english, total_vocab_hindi, total_vocab_english, total_vocab_size_hindi, total_vocab_size_english, DF_hindi, DF_english, D_hindi, D_english)
    webbrowser.get(using='google-chrome').open('../Output/output.html')
    return

if __name__== "__main__":
  main()
