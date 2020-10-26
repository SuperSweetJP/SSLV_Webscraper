#!/usr/bin/python
# -*- coding: latin1 -*-

import requests
from bs4 import BeautifulSoup


def getDetails(detailsPageLink):

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


    dictDetails = dict(zip(detailsNameList, detailsValueList))

    equip_set = ""
    for equipment in soup.find_all('b', class_='auto_c'):
        equip_set += equipment.text + "|"
    
    #marka, gads, motors, karba, nobr, krasa, virsb, apskate, apriko
    detailsList = [
            dictDetails.get('Marka ', ''),
            dictDetails.get('Izlaiduma gads:', ''),
            dictDetails.get('Motors:', ''),
            dictDetails.get('Âtr.kârba:', ''),
            dictDetails.get('Nobraukums, km:', ''),
            dictDetails.get('Krâsa:', ''),
            dictDetails.get('Virsbûves tips:', ''),
            dictDetails.get('Tehniskâ apskate:', ''),
            equip_set
        ]

    #print(detailsList[4])
    return detailsList

#getDetails("https://www.ss.lv/msg/lv/transport/cars/volvo/xc70/ehcof.html1406")