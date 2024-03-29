﻿import requests
from bs4 import BeautifulSoup

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def getVehicleDetails(detailsPageLink):

    detailsNameList = list()
    detailsValueList = list()

    # Source scrape
    r = requests.get(detailsPageLink)
    soup = BeautifulSoup(r.content, "html.parser")

    # Get Base Data
    baseTable = soup.find('table', class_='options_list')
    for varName in baseTable.find_all('td', class_='ads_opt_name'):
        detailsNameList.append(varName.text)
    for varValue in baseTable.find_all('td', class_='ads_opt'):
        detailsValueList.append(varValue.text)
    #gather contacts data
    contactsTable = soup.find('table', class_='contacts_table')
    for varName in contactsTable.find_all('td', class_='ads_contacts_name'):
        detailsNameList.append(varName.text)
    for varValue in contactsTable.find_all('td', class_='ads_contacts'):
        detailsValueList.append(varValue.text)

    dictDetails = dict(zip(detailsNameList, detailsValueList))

    equip_set = ""
    for equipment in soup.find_all('b', class_='auto_c'):
        equip_set += equipment.text + "|"

    #----------------Apraksts-------------------------------
    startString = '<div id="content_sys_div_msg" style="float:right;margin:0px 0px 20px 20px;"></div>'
    endString = '<table'

    aprChildren = str(soup.find(id='content_main_div'))

    soup2 = BeautifulSoup(aprChildren[aprChildren.find(startString)+len(startString):aprChildren.find(endString)], "html.parser")
    description = soup2.text

    #check description len, column limit is 10k
    if len(description) > 10000:
        description = description[:10000]

    priceElemenet = soup.find(class_="ads_price")
    price = priceElemenet.find(class_="ads_price").text

    #get category from link
    sepLocList = find(detailsPageLink, '/')
    checkLink = detailsPageLink[sepLocList[5]+1:sepLocList[6]]

    #PROCESS DATA
    #Gads to int, remove month name
    gadsMod = dictDetails.get('Izlaiduma gads:', '').split(" ", 1)[0]

    if checkLink == 'cars':
        #marka, gads, motors, karba, nobr, krasa, virsb, apskate, vieta, aprikojums, apraksts, cena, gadsMod
        detailsList = [
                dictDetails.get('Marka ', ''),
                dictDetails.get('Izlaiduma gads:', ''),
                dictDetails.get('Motors:', ''),
                dictDetails.get('Ātr.kārba:', ''),
                dictDetails.get('Nobraukums, km:', ''),
                dictDetails.get('Krāsa:', ''),
                dictDetails.get('Virsbūves tips:', ''),
                dictDetails.get('Tehniskā apskate:', ''),
                dictDetails.get('Vieta:', ''),
                equip_set,
                description,
                price,
                gadsMod
            ]
    elif checkLink == 'moto-transport':
        #marka, modelis, gads, motors, vieta, apraksts, cena
        detailsList = [
            dictDetails.get('Marka:', ''),
            dictDetails.get('Modelis:', ''),
            dictDetails.get('Izlaiduma gads:', ''),
            dictDetails.get('Motora tilpums, cm3:', ''),
            dictDetails.get('Vieta:', ''),
            description,
            price,
            gadsMod
        ]

    return detailsList


# print(getVehicleDetails("https://www.ss.lv/msg/lv/transport/cars/citroen/c-elysee/bolkpg.html"))
# print(getVehicleDetails("https://www.ss.lv/msg/lv/transport/cars/mazda/cx-5/cbcmig.html"))