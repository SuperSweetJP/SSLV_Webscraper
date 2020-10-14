import mysql.connector
import re
import os
import requests
import datetime
import time
import varExtractor
from bs4 import BeautifulSoup

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="anubissayshello",
  database="sslv"
)

mycursor = mydb.cursor(buffered=True)
categoryLink = ""
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
    global categoryLink
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

            #fetch details for the link, return them as a list?
            #try:
            detailsList = varExtractor.ss_scrapevars(parm[0])
            sqlUpdateDetails = '''UPDATE CarsTable SET Marka = %s, Gads = %s, Motors = %s, Karba = %s, Nobr = %s, Krasa = %s, Virsb = %s, Skate = %s, Apr = %s 
                WHERE link = %s AND Header = %s'''
            detailsList.append(parm[0])
            detailsList.append(parm[1])
            mycursor.execute(sqlUpdateDetails, detailsList)
            mydb.commit()
            #except:
            #    print("error in link:" + parm[0])

        #if record found, update last seen
        else:
            sqlUpdate = "UPDATE CarsTable SET LastSeen = %s WHERE link = %s AND Header = %s"
            parmUpd = (runDateTime, parm[0], parm[1])
            mycursor.execute(sqlUpdate, parmUpd)
            mydb.commit()


all_models = [
    "https://www.ss.lv/lv/transport/cars/alfa-romeo/sell/",
    "https://www.ss.lv/lv/transport/cars/audi/sell/",
    "https://www.ss.lv/lv/transport/cars/bmw/sell/",
    "https://www.ss.lv/lv/transport/cars/cadillac/sell/",
    "https://www.ss.lv/lv/transport/cars/chevrolet/sell/",
    "https://www.ss.lv/lv/transport/cars/chrysler/sell/",
    "https://www.ss.lv/lv/transport/cars/citroen/sell/",
    "https://www.ss.lv/lv/transport/cars/dacia/sell/",
    "https://www.ss.lv/lv/transport/cars/daewoo/sell/",
    "https://www.ss.lv/lv/transport/cars/dodge/sell/",
    "https://www.ss.lv/lv/transport/cars/fiat/sell/",
    "https://www.ss.lv/lv/transport/cars/ford/sell/",
    "https://www.ss.lv/lv/transport/cars/honda/sell/",
    "https://www.ss.lv/lv/transport/cars/hyundai/sell/",
    "https://www.ss.lv/lv/transport/cars/infiniti/sell/",
    "https://www.ss.lv/lv/transport/cars/jaguar/sell/",
    "https://www.ss.lv/lv/transport/cars/jeep/sell/",
    "https://www.ss.lv/lv/transport/cars/kia/sell/",
    "https://www.ss.lv/lv/transport/cars/lancia/sell/",
    "https://www.ss.lv/lv/transport/cars/land-rover/sell/",
    "https://www.ss.lv/lv/transport/cars/lexus/sell/",
    "https://www.ss.lv/lv/transport/cars/mazda/sell/",
    "https://www.ss.lv/lv/transport/cars/mercedes/sell/",
    "https://www.ss.lv/lv/transport/cars/mini/sell/",
    "https://www.ss.lv/lv/transport/cars/mitsubishi/sell/",
    "https://www.ss.lv/lv/transport/cars/nissan/sell/",
    "https://www.ss.lv/lv/transport/cars/opel/sell/",
    "https://www.ss.lv/lv/transport/cars/peugeot/sell/",
    "https://www.ss.lv/lv/transport/cars/porsche/sell/",
    "https://www.ss.lv/lv/transport/cars/renault/sell/",
    "https://www.ss.lv/lv/transport/cars/saab/sell/",
    "https://www.ss.lv/lv/transport/cars/seat/sell/",
    "https://www.ss.lv/lv/transport/cars/skoda/sell/",
    "https://www.ss.lv/lv/transport/cars/ssangyong/sell/",
    "https://www.ss.lv/lv/transport/cars/subaru/sell/",
    "https://www.ss.lv/lv/transport/cars/suzuki/sell/",
    "https://www.ss.lv/lv/transport/cars/toyota/sell/",
    "https://www.ss.lv/lv/transport/cars/volkswagen/sell/",
    "https://www.ss.lv/lv/transport/cars/volvo/sell/",
    "https://www.ss.lv/lv/transport/cars/moskvich/sell/",
    "https://www.ss.lv/lv/transport/cars/uaz/sell/",
    "https://www.ss.lv/lv/transport/cars/gaz/sell/",
    "https://www.ss.lv/lv/transport/cars/vaz/sell/",
    "https://www.ss.lv/lv/transport/cars/others/sell/"
]

single_model = ["https://www.ss.lv/lv/transport/cars/mini/sell/"]



for model in single_model:
    #try:
    #    start_time = time.time()
    #    categoryPageLoop(model)
    #    run_time = time.time() - start_time
    #    print("category: {} completed at {} seconds".format(model, run_time))
    #except:
    #    print("issue in category: " + model)

    start_time = time.time()
    categoryPageLoop(model)
    run_time = time.time() - start_time
    print("category: {} completed at {} seconds".format(model, run_time))
