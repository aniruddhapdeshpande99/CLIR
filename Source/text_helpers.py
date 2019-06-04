from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words
from operator import itemgetter

import nltk
import os
import string
import numpy as np
import copy
import pandas as pd
import pickle
import re
import math
import json

def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text


def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")

def stemming(data):
    stemmer= PorterStemmer()

    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

def preprocess_eng(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    return data

def preprocess_hin(data):
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    return data

def read_data_eng():
    data_folder = "../Data/Articles/English/"
    dataset = {}
    doc_index = 0
    file_names = [x[2] for x in os.walk(str(data_folder))]
    file_names = file_names[0] #Above value is a 2D array
    for i in file_names:
        with open(data_folder+i) as json_file:
            article = json.load(json_file)
            curr_article = {}
            curr_article['title'] = article['title'].strip() #Using strip to remove leading and trailing spaces
            curr_article['text'] = article['text'].strip()
            curr_article['index'] = doc_index
            dataset[i[:-5]] = curr_article #i[:-5] so as to remove .json from the key of the dictionary
            doc_index = doc_index + 1
    return dataset

def read_data_hin():
    data_folder = "../Data/Articles/Hindi/"
    dataset = {}
    doc_index = 0
    file_names = [x[2] for x in os.walk(str(data_folder))]
    file_names = file_names[0] #Above value is a 2D array
    for i in file_names:
        with open(data_folder+i) as json_file:
            article = json.load(json_file)
            curr_article = {}
            curr_article['title'] = article['title'].strip() #Using strip to remove leading and trailing spaces
            curr_article['text'] = article['text'].strip()
            curr_article['index'] = doc_index
            dataset[i[:-5]] = curr_article #i[:-5] so as to remove .json from the key of the dictionary
            doc_index = doc_index + 1
    return dataset

def return_len_dataset(dataset):
    return len(dataset)

def make_output(original_lang, translated_lang, original_query, translated_query, Q_hindi, Q_english, dataset_hindi, dataset_english, k):

    top_english_keys = []
    top_hindi_keys = []

    final_top_k = mergeArrays(Q_english, Q_hindi)

    for i in range(0,len(final_top_k)):
        index = final_top_k[i][0]
        lang = final_top_k[i][2]
        if lang == 'eng':
            for key in dataset_english.keys():
                if dataset_english[key]['index'] == index:
                    final_top_k[i].append(key)

        elif lang == 'hin':
            for key in dataset_hindi.keys():
                if dataset_hindi[key]['index'] == index:
                    final_top_k[i].append(key)


    html_text="<!DOCTYPE html><html><body><h1>CLIR Output</h1><p><b>Original Query: </b>"+original_query+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Original Language: </b>"+original_lang+"</p>"
    html_text = html_text + "<p><b>Translated Query: </b>"+translated_query+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Target Language: </b>"+translated_lang+"</p>"
    html_text = html_text + "<h2>Top "+str(k)+" Articles are: </h2><ol>"

    for i in range(0,k):
        if final_top_k[i][2] == 'eng':
            curr_key = final_top_k[i][3]
            curr_title = dataset_english[curr_key]['title']
            html_text=html_text+"<li><a href='../Data/HTML/English/"+curr_key+".html'>"+curr_title+"</a></li>"

        elif final_top_k[i][2] == 'hin':
            curr_key = final_top_k[i][3]
            curr_title = dataset_hindi[curr_key]['title']
            html_text=html_text+"<li><a href='../Data/HTML/Hindi/"+curr_key+".html'>"+curr_title+"</a></li>"

    html_text = html_text + "</ol></body></html>"
    output_file = open("../Output/output.html", "w")
    output_file.write(html_text)
    output_file.close()
    return

def mergeArrays(arr1, arr2):
    arr1.extend(arr2)
    arr3 = sorted(arr1,key=itemgetter(1), reverse=True)
    return arr3
