#This Code parses through the given JSON file and makes an HTML page to display that news article.

#Importing Libraries
import json
import os

#Preprocesses the text as per HTML and adds Article's title
def add_title(title):
    title = title.replace("\"","&quot;")
    title = title.replace("“", "&ldquo;")
    title = title.replace("”", "&rdquo;")
    return "<h1>" + title + "</h1>"

#Preprocesses the text as per HTML and adds Article's authors
def add_authors(authors):
    if len(authors)==0:
        return "<p><b>Authors : </b>No Author Specified</p>"
    else:
        author_string = "<p><b>Authors : </b>"
        for i in authors:
            author_string = author_string + i + ", "
        author_string = author_string[:-1] + "</p>"
        return author_string

#Preprocesses the date as per HTML and adds Article's Publishing Date
def add_publish_date(date):
    date_time = date.replace('/', '&#47;')
    date_time = date_time.replace(':', '&#58;')
    return "<p><b>Published on : </b>" + date_time + "</p>"

#Preprocesses the text as per HTML and adds Article's description
def add_description(description):
    description = description.replace("\"","&quot;")
    description = description.replace("“", "&ldquo;")
    description = description.replace("”", "&rdquo;")
    return "<p><b>" + description + "</b></p>"

#Preprocesses the url as per HTML and adds Article's image
def add_image(image_url):
    return "<img src=\"" + image_url + "\" width=\"500\" height=\"600\">"

#Preprocesses the text as per HTML and adds Article's main text
def add_text(text):
    text = text.replace("\"","&quot;")
    text = text.replace("“", "&ldquo;")
    text = text.replace("”", "&rdquo;")
    return "<p>" + text + "</p>"

#Calls every function above to compile the final html page and saves it
def make_html():
    data_folder = "../Data/Articles/Hindi/"
    dataset = {}
    doc_index = 0
    file_names = [x[2] for x in os.walk(str(data_folder))]
    file_names = file_names[0] #Above value is a 2D array
    for i in file_names:
        with open(data_folder+i) as json_file:
            article = json.load(json_file)
            output_file = open("../Data/HTML/Hindi/"+i[:-5]+".html", "w")
            html_text = "<!DOCTYPE html><html><body>"
            html_text = html_text + add_title(article['title']) + add_authors(article['authors']) + add_publish_date(article['date_publish']) + add_description(article['description']) + add_image(article['image_url']) + add_text(article['text']) + "<a href='../../../Output/output.html'> Back to Output page </a> </body></html>"
            output_file.write(html_text)
            output_file.close()

    data_folder = "../Data/Articles/English/"
    dataset = {}
    doc_index = 0
    file_names = [x[2] for x in os.walk(str(data_folder))]
    file_names = file_names[0] #Above value is a 2D array
    for i in file_names:
        with open(data_folder+i) as json_file:
            article = json.load(json_file)
            output_file = open("../Data/HTML/English/"+i[:-5]+".html", "w")
            html_text = "<!DOCTYPE html><html><body>"
            html_text = html_text + add_title(article['title']) + add_authors(article['authors']) + add_publish_date(article['date_publish']) + add_description(article['description']) + add_image(article['image_url']) + add_text(article['text']) + "<a href='../../../Output/output.html'> Back to Output page </a> </body></html>"
            output_file.write(html_text)
            output_file.close()

    return
#Main function to call make_html()
def main():
  make_html()


#Calls Main function
if __name__== "__main__":
  main()
