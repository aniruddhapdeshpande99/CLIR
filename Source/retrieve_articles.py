#This Code Retrieves all the articles from the [lang]_links.txt (lang = english or hindi)
#And creates their JSON object files for make_html.py to use using NewsPlease news article crawler

#Importing Libraries
from newsplease import NewsPlease
import json
import re
from datetime import datetime

#Extracts filename out of the url
def return_filename(url):
    filename = url.rsplit('/',1)[1][:-5]
    return filename

#Saves the JSON object using the filename retrieved from return_filename()
def save_json(article):
    data = {}
    data['title'] = article.title
    data['authors'] = article.authors
    data['date_publish'] = article.date_publish.strftime("%d/%m/%Y, %H:%M:%S")
    data['description'] = article.description
    data['image_url'] = article.image_url
    data['text'] = article.text
    data['url'] = article.url
    filename = return_filename(article.url)
    with open("../Data/Articles/English/" + filename + 'json', 'w') as outfile:
        json.dump(data, outfile)

    print("{}json has been saved".format(filename))
    return

#Retrieves all the articles from [lang]_links.txt
def retrieve_articles():
    links = []
    with open("../Data/Links/English/english_links.txt") as link_file:
        links = link_file.readlines()

    articles = []
    for link in links:
        article = NewsPlease.from_url(link)
        save_json(article)
    return

#Main function to call retrieve_articles()
def main():
  retrieve_articles()

#Calling Main function
if __name__== "__main__":
  main()
