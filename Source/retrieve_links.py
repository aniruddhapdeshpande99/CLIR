#This Code Retrieves Links and saves it in a file that can be later used by NewsPlease
#in retrieve_articles.py

#Importing Libraries
from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen

#This function retrieves the links of n number of English news articles on a given page
def retrieve_english_news_links(link):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features='lxml')
    article_a_tags = soup.findAll("a", {"class": "card-big"}, href=True)
    article_links = []
    for i in article_a_tags:
        article_links.append(i['href'])
    return article_links

#This function iterates through all the pages of news articles and calls retrieve_english_news_links()
#in order to retrieve the links of the articles from that respective page and saves it all in a file
def retrieve_all_english_links():
    page_link_template = 'https://www.indiatimes.com/seoarchive/entertainment/pg-'
    f = open("../Data/Links/English/english_links.txt", "w")
    for i in range(1,11):
        curr_page_link = page_link_template + str(i) + "/"
        article_links = retrieve_english_news_links(curr_page_link)
        for url in article_links:
            f.write(url+"\n")
    f.close()
    return

#This function retrieves the links of n number of Hindi news articles on a given page
def retrieve_hindi_news_links(link):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features='lxml')
    article_div_tags = soup.findAll("div", {"class": "textsec"})
    article_links = []
    for i in article_div_tags:
        article_links.append(i.findAll("a")[0]['href'])
    return article_links

#This function iterates through all the pages of news articles and calls retrieve_hindi_news_links()
#in order to retrieve the links of the articles from that respective page and saves it all in a file
def retrieve_all_hindi_links():
    page_link_template = 'https://navbharattimes.indiatimes.com/movie-masti/news-from-bollywood/articlelist/2303550.cms?curpg='
    f = open("../Data/Links/Hindi/hindi_links.txt", "w")
    for i in range(1,11):
        curr_page_link = page_link_template + str(i)
        article_links = retrieve_hindi_news_links(curr_page_link)
        for url in article_links:
            f.write(url+"\n")
    f.close()
    return

#Main function to call retrieve_all_hindi_links() and retrieve_all_english_links()
def main():
  retrieve_all_english_links()
  print("English Article URLS Retrieved")
  retrieve_all_hindi_links()
  print("Hindi Article URLS Retrieved")

#Calling Main function
if __name__== "__main__":
  main()
