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
categoryList = ['Cars', 'Motorcycles']
carCategoryList = open("carCategoryList.txt", "r").readlines()
motorcycleCategoryList = open("motorcycleCategoryList.txt", "r").readlines()

#scrape the list of items for links and headers
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


def makePageLoop(catLink):
    #set global variables for category run
    global categoryLink
    categoryLink = catLink
    global runDateTime
    runDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #switch
    processLinksDb(scrapeListPage(catLink))
    i = 2
    #scrape subsequent pages, break when return to original page
    while True:
        catLinkNextPage = catLink + "page" + str(i) + ".html"
        nextPageReq = requests.get(catLinkNextPage)
        if catLink == nextPageReq.url:
            break
        #switch
        processLinksDb(scrapeListPage(catLinkNextPage))
        i += 1


#ToDo: add db logic here, add details gather call here
def processLinksDb(linkDict):
    for x, y in linkDict.items():
        print(x)
        #check if link and header combo already in db
        sqlSelect = "SELECT link, Header, DetailsUpdated, FirstSeen from CarsTable WHERE link = %s AND Header = %s ORDER BY FirstSeen DESC LIMIT 1"
        parm = (x, y)

        mycursor.execute(sqlSelect, parm)
        rows = mycursor.rowcount
        #if no combo in db, insert new record
        if rows == 0:
            sqlInsert = "INSERT INTO CarsTable (link, Header, Category, FirstSeen) VALUES (%s, %s, %s, %s)"
            parmIns = (parm[0], parm[1], categoryLink, runDateTime)
            mycursor.execute(sqlInsert, parmIns)
            mydb.commit()

            #update details
            mysqlUpdateDetails(parm[0], parm[1])

        #if record found
        else:
            for row in mycursor:
                #check if details updated
                if row[2] == 0:
                    print("need to update details")
                    mysqlUpdateDetails(parm[0], parm[1])

            #update last seen
            sqlUpdate = "UPDATE CarsTable SET LastSeen = %s WHERE link = %s AND Header = %s"
            parmUpd = (runDateTime, parm[0], parm[1])
            mycursor.execute(sqlUpdate, parmUpd)
            mydb.commit()

def mysqlUpdateDetails(link, header):
        #fetch details for the link, return them as a list?
        try:
            detailsList = varExtractor.ss_scrapevars(link)
            sqlUpdateDetails = '''UPDATE CarsTable SET Marka = %s, Gads = %s, Motors = %s, Karba = %s, Nobr = %s, Krasa = %s, Virsb = %s, Skate = %s, Apr = %s 
                DetailsUpdated = %s WHERE link = %s AND Header = %s'''
            #detailsUpdated bool
            detailsList.append("1")
            detailsList.append(link)
            detailsList.append(header)
            mycursor.execute(sqlUpdateDetails, detailsList)
            mydb.commit()
        except:
            print("error in link:" + link)


make = carCategoryList[6]

#for make in single_model:
#    #try:
#    #    start_time = time.time()
#    #    categoryPageLoop(model)
#    #    run_time = time.time() - start_time
#    #    print("category: {} completed at {} seconds".format(model, run_time))
#    #except:
#    #    print("issue in category: " + model)

try:
    #start_time = time.time()
    makePageLoop(make)
    #run_time = time.time() - start_time
    #print("category: {} completed at {} seconds".format(make, run_time))
    print("done!")
except:
    print("issue in category: " + make)
