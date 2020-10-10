import mysql.connector
import re
import os
import requests
import datetime
import varExtractor
from bs4 import BeautifulSoup

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="anubissayshello",
  database="sslv"
)

mycursor = mydb.cursor(buffered=True)

#hard coded category for now
#ToDo rework into main loop that passes all categories later on
categoryLink="https://www.ss.lv/lv/transport/cars/uaz/"
runDateTime = ""

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
    #set global variables for category run
    categoryLink = catLink
    global runDateTime
    runDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

    mycursor.close()


#ToDo: add db logic here, add details gather call here
def processLinksDb(linkDict):
    for x, y in linkDict.items():

        #check if link and header combo already in db
        sqlSelect = "SELECT link, Header from CarsTable WHERE link = %s AND Header = %s"
        parm = (x, y)

        mycursor.execute(sqlSelect, parm)
        rows = mycursor.rowcount
        #if no combo in db, insert new record
        if rows == 0:
            sqlInsert = "INSERT INTO CarsTable (link, Header, Category, FirstSeen) VALUES (%s, %s, %s, %s)"
            parmIns = (parm[0], parm[1], categoryLink, runDateTime)
            mycursor.execute(sqlInsert, parmIns)
            mydb.commit()
        #if record found, update last seen
        else:
            sqlUpdate = "UPDATE CarsTable SET LastSeen = %s WHERE link = %s AND Header = %s"
            parmUpd = (runDateTime, parm[0], parm[1])
            mycursor.execute(sqlUpdate, parmUpd)
            mydb.commit()





categoryPageLoop(categoryLink)
#print(scrapeListPage(categoryLink))