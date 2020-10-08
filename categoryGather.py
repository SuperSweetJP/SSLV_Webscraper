import mysql.connector
import re
import os
import requests
from bs4 import BeautifulSoup

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="anubissayshello",
  database="sslv"
)

mycursor = mydb.cursor()

#hard coded category for now
#ToDo rework into main loop that passes all categories later on
categoryLink="https://www.ss.lv/lv/transport/cars/fiat/"
catTitle = ""

def scrapeListPage(pageLink):
    unique_link_set = list()
    unique_header_set = list()

    source = requests.get(pageLink)
    soup = BeautifulSoup(source.content, "html.parser")
    for link in soup.find_all("a", href=re.compile('/msg/')):
        if 'msg/lv/transport/cars/' in link.get('href'):
            link = (link.get('href'))
            link = "http://www.ss.lv{}".format(link)
            if link not in unique_link_set:
                unique_link_set.append(link)

    for header in soup.find_all('a', class_="am"):
        extract = header.text.splitlines()
        extract2 = ''.join(extract)
        if extract2 not in unique_header_set:
            unique_header_set.append(extract2)
    
    resultDict = {unique_link_set[i]: unique_header_set[i] for i in range(len(unique_link_set))}

    return resultDict


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
def processLinksDb(linkDict):
    for x, y in linkDict.items():
        print(x, y)
        #check if link already in db
        sqlSelect = "SELECT link, Category from CarsTable WHERE link = %s AND Category = %s"
        parm = (x, y)

        mycursor.execute(sqlSelect, parm)
        rows = mycursor.rowcount

        print(rows)
        #if  == 0:
        #if not write new record
            #print("record doesn't exist, inserting")
        #if yes, check if same header

            #if yes, update last seen

            #if no, write new record


categoryPageLoop(categoryLink)
#print(scrapeListPage(categoryLink))