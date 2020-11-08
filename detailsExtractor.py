import requests
from bs4 import BeautifulSoup


def getCarDetails(detailsPageLink):

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

    #----------------Apraksts-------------------------------
    startString = '<div id="content_sys_div_msg" style="float:right;margin:0px 0px 20px 20px;"></div>'
    endString = '<table'

    aprChildren = str(soup.find(id='content_main_div'))

    soup2 = BeautifulSoup(aprChildren[aprChildren.find(startString)+len(startString):aprChildren.find(endString)], "html.parser")
    description = soup2.text
   
    priceElemenet = soup.find(class_="ads_price")
    price = priceElemenet.find(class_="ads_price").text

    #marka, gads, motors, karba, nobr, krasa, virsb, apskate, apriko
    detailsList = [
            dictDetails.get('Marka ', ''),
            dictDetails.get('Izlaiduma gads:', ''),
            dictDetails.get('Motors:', ''),
            dictDetails.get('Ātr.kārba:', ''),
            dictDetails.get('Nobraukums, km:', ''),
            dictDetails.get('Krāsa:', ''),
            dictDetails.get('Virsbūves tips:', ''),
            dictDetails.get('Tehniskā apskate:', ''),
            equip_set,
            description,
            price
        ]

    return detailsList

def getMotorcycleDetails(detailsPageLink):

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

    print(detailsList[6])
    return detailsList


#getCarDetails("http://www.ss.lv/msg/lv/transport/cars/dodge/caliber/gkifc.html")
#print(getMotorcycleDetails("https://www.ss.lv/msg/lv/transport/moto-transport/motorcycles/yamaha/fomho.html"))a