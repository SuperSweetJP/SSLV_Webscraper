import requests
import os
from bs4 import BeautifulSoup

# http://www.ss.lv/msg/lv/transport/cars/alfa-romeo/159/bocijp.html


def ss_scrapecontent():

    # Source scrape
    r = requests.get(str("http://www.ss.lv/msg/lv/transport/cars/alfa-romeo/159/bocijp.html"))
    soup = BeautifulSoup(r.content, "html.parser")

    print("http://www.ss.lv/msg/lv/transport/cars/alfa-romeo/159/bocijp.html" + "\n")

    basicdatalist = open("basicdatalist.txt", "a", encoding='utf-8')
    basicdatalist.write("http://www.ss.lv/msg/lv/transport/cars/alfa-romeo/159/bocijp.html" + "\n")
    basicdatalist.write("\n")
    basicdatalist.close()

    # Get Basic Data
    for getmakemodel in soup.find_all('table', class_='options_list'):
        for makemodel in getmakemodel.find_all('td', class_='ads_opt'):
            alldata = makemodel.text

            print(alldata)
            basicdatalist = open("basicdatalist.txt", "a", encoding='utf-8')
            basicdatalist.write(alldata + "\n")
            basicdatalist.close()

    # Get price data
    getprice = soup.find('td', class_='ads_price')
    price = getprice.span.text
    print(price + "\n")
    basicdatalist = open("basicdatalist.txt", "a", encoding='utf-8')
    basicdatalist.write("\n")
    basicdatalist.write(price + "\n")
    basicdatalist.close()

    # Get equipment data
    for equipment in soup.find_all('b', class_='auto_c'):

        equipped = equipment.text
        print(equipped)
        basicdatalist = open("basicdatalist.txt", "a", encoding='utf-8')
        basicdatalist.write("\n")
        basicdatalist.write(equipped)
        basicdatalist.close()

    basicdatalist = open("basicdatalist.txt", "a", encoding='utf-8')
    basicdatalist.write("\n" + "----------------------------------")
    basicdatalist.write("\n" + "----------------------------------")
    basicdatalist.close()

    # Remove unneeded data
    with open("basicdatalist.txt", "r", encoding='utf-8') as dt_list:
        lines = dt_list.readlines()
    with open("basicdataset.txt", "w", encoding='utf-8') as dt_list:
        for line in lines:
            if line.strip("\n") != "Parādīt vin kodu" and line.strip("\n") != "Parādīt valsts numura zīmi":
                dt_list.write(line)

    # Remove clutter file
    if os.path.exists("basicdatalist.txt"):
        os.remove("basicdatalist.txt")


ss_scrapecontent()
