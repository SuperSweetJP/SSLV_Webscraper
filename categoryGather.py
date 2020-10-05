import mysql.connector
import re
import os
import requests
from bs4 import BeautifulSoup

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="anubissayshello",
  database="sslv"
)

#hard coded category for now
#ToDo rework into main loop that passes all categories later on
categoryLink="https://www.ss.lv/lv/transport/cars/fiat/"

def scrapeListPage(pageLink):
    unique_link_set = list()

    source = requests.get(pageLink)
    soup = BeautifulSoup(source.content, "html.parser")
    for link in soup.find_all("a", href=re.compile('/msg/')):
        if 'msg/lv/transport/cars/' in link.get('href'):
            link = (link.get('href'))
            link = "http://www.ss.lv{}".format(link)
            if link not in unique_link_set:
                unique_link_set.append(link)
    
    return unique_link_set

def categoryPageLoop(catLink):
    #screape the original page
    processLinksDb(scrapeListPage(catLink))
    i = 2
    #scrape subsequent pages, break when return to original page
    while True:
        catLinkNextPage = catLink + "page" + str(i) + ".html"
        nextPageReq = requests.get(catLinkNextPage)
        if catLink == nextPageReq.url:
            break
        processLinksDb(scrapeListPage(catLinkNextPage))
        i += 1

#ToDo: add db logic here, add details gather call here
def processLinksDb(linkList):
    for link in linkList:
        print(link)
        #check if link already in db
        #if not write new record

        #if yes, check if same header

            #if yes, update last seen

            #if no, write new record


#categoryPageLoop(categoryLink)
