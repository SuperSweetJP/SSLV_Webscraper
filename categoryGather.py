import mysql.connector
import re
import os
import requests
import datetime
import time
import detailsExtractor
from bs4 import BeautifulSoup
import linkLists

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
carCategoryList = linkLists.carCategoryList
motorcycleCategoryList = linkLists.motorcycleCategoryList


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
        #JP:there can be two identical headers, removing unique check
        #if extract2 not in unique_header_set:
        unique_header_set.append(extract2)
    
    resultDict = {unique_link_set[i]: unique_header_set[i] for i in range(len(unique_link_set))}
    return resultDict


def subCatPageLoop(catLink, subCat):
    #set global variables for category run
    global categoryLink
    categoryLink = catLink
    global runDateTime
    runDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    processLinksDb(scrapeListPage(catLink), subCat)
    i = 2
    #scrape subsequent pages, break when return to original page
    while True:
        catLinkNextPage = catLink + "page" + str(i) + ".html"
        nextPageReq = requests.get(catLinkNextPage)
        if catLink == nextPageReq.url:
            break
        processLinksDb(scrapeListPage(catLinkNextPage), subCat)
        i += 1


#ToDo: add db logic here, add details gather call here
def processLinksDb(linkDict, subCategory):
    for x, y in linkDict.items():
        #print(x)
        #check if link and header combo already in db
        #Cars
        if subCategory == categoryList[0]:
            sqlSelect = "SELECT link, Header, DetailsUpdated, FirstSeen from CarsTable WHERE link = %s AND Header = %s ORDER BY FirstSeen DESC LIMIT 1"
        #Motorcycles
        elif subCategory == categoryList[1]:
            sqlSelect = "SELECT link, Header, DetailsUpdated, FirstSeen from CarsTable WHERE link = %s AND Header = %s ORDER BY FirstSeen DESC LIMIT 1"

        parm = (x, y)

        mycursor.execute(sqlSelect, parm)
        rows = mycursor.rowcount
        record = mycursor.fetchall()
        #if no combo in db, insert new record
        if rows == 0:
            #Cars
            if subCategory == categoryList[0]:
                sqlInsert = "INSERT INTO CarsTable (link, Header, Category, FirstSeen) VALUES (%s, %s, %s, %s)"
            #Motorcycles
            elif subCategory == categoryList[1]:
                sqlInsert = "INSERT INTO CarsTable (link, Header, Category, FirstSeen) VALUES (%s, %s, %s, %s)"
            parmIns = (parm[0], parm[1], categoryLink, runDateTime)
            mycursor.execute(sqlInsert, parmIns)
            mydb.commit()

            #update details
            mysqlUpdateDetails(parm[0], parm[1], subCategory)

        #if record found
        else:
            if record[0][2] == 0:
                print("need to update details for link: {}".format(parm[0]))
                mysqlUpdateDetails(parm[0], parm[1], subCategory)

            #update last seen
            #Cars
            if subCategory == categoryList[0]:
                sqlUpdate = "UPDATE CarsTable SET LastSeen = %s WHERE link = %s AND Header = %s"
            #Motorcycles
            elif subCategory == categoryList[1]:
                sqlUpdate = "UPDATE CarsTable SET LastSeen = %s WHERE link = %s AND Header = %s"
            parmUpd = (runDateTime, parm[0], parm[1])
            mycursor.execute(sqlUpdate, parmUpd)
            mydb.commit()


def mysqlUpdateDetails(link, header, subCategory):
        #fetch details for the link, return them as a list?
        try:
            if subCategory == categoryList[0]:
                detailsList = detailsExtractor.getCarDetails(link)
                sqlUpdateDetails = '''UPDATE CarsTable SET Marka = %s, Gads = %s, Motors = %s, Karba = %s, Nobr = %s, Krasa = %s, Virsb = %s, Skate = %s, Apr = %s, Apraksts + %s, 
                    DetailsUpdated = %s WHERE link = %s AND Header = %s'''
            elif subCategory == categoryList[1]:
                detailsList = detailsExtractor.getMotorcycleDetails(link)
                sqlUpdateDetails = '''UPDATE CarsTable SET Marka = %s, Gads = %s, Motors = %s, Karba = %s, Nobr = %s, Krasa = %s, Virsb = %s, Skate = %s, Apr = %s, 
                    DetailsUpdated = %s WHERE link = %s AND Header = %s'''
            #detailsUpdated bool
            detailsList.append("1")
            detailsList.append(link)
            detailsList.append(header)
            mycursor.execute(sqlUpdateDetails, detailsList)
            mydb.commit()
        except Exception as ex:
            print("error in link: {}".format(link))
            print(ex)



startTime = time.time()

#Cars
for subCat in carCategoryList:
    try:
        start_timeCat = time.time()
        subCatPageLoop(subCat, categoryList[0])
        run_timeCat = time.time() - start_timeCat
        print("category: {} completed at {} seconds".format(subCat, run_timeCat))
    except Exception as ex:
        print("issue in category: {}".format(subCat))
        print(ex)

#Motorcycles
#for subCat in motorcycleCategoryList:
#    try:
#        start_timeCat = time.time()
#        subCatPageLoop(subCat, categoryList[1])
#        run_timeCat = time.time() - start_timeCat
#        print("category: {} completed at {} seconds".format(subCat, run_timeCat))
#    except Exception as ex:
#        print("issue in category: {}".format(subCat))
#        print(ex)


#try:
#    subCatLink = carCategoryList[9]
#    start_timeCat = time.time()
#    subCatPageLoop(subCatLink, categoryList[0])
#    run_timeCat = time.time() - start_timeCat
#    print("category: {} completed at {} seconds \n".format(subCatLink, run_timeCat))
#except Exception as ex:
#    print("issue in category: {} \n".format(subCatLink))
#    print(ex + "\n")

run_time = time.time() - startTime
print(f"whole process finished in: {run_time} seconds")
