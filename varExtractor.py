import requests
from bs4 import BeautifulSoup

# Infiniti single link variable extraction test


def ss_scrapevars(detailsPageLink):

    vari_set = list()
    equip_set = list()
    detailsList = list()

    # Source scrape

    r = requests.get(detailsPageLink)
    soup = BeautifulSoup(r.content, "html.parser")

    # Get Basic Data

    for getvardata in soup.find_all('table', class_='options_list'):
        for vardata in getvardata.find_all('td', class_='ads_opt'):
            alldata = vardata.text
            if alldata not in vari_set:
                vari_set.append(alldata)

    if 'Parādīt valsts numura zīmi' in vari_set:
        vari_set.remove('Parādīt valsts numura zīmi')
    if 'Parādīt vin kodu' in vari_set:
        vari_set.remove('Parādīt vin kodu')
    for spc in range(3, 12):
        if str(spc) in vari_set:
            vari_set.pop(7)

    ckey_set = ("mnf", "yr", "engi", "gbox", "mlg", "clr", "bdy", "svc")
    dtkey = {ckey_set[i]: vari_set[i] for i in range(len(ckey_set))}

    equip_set = ""
    for equipment in soup.find_all('b', class_='auto_c'):
        equip_set += equipment.text + "|"

    # Setting variables
    marka = dtkey.get('mnf')
    gads = dtkey.get('yr')
    motors = dtkey.get('engi')
    karba = dtkey.get('gbox')
    nobr = dtkey.get('mlg')
    krasa = dtkey.get('clr')
    virsb = dtkey.get('bdy')
    apskate = dtkey.get('svc')
    apriko = equip_set

    detailsList = [marka, gads, motors, karba, nobr, krasa, virsb, apskate, apriko]

    return detailsList

#print(ss_scrapevars("http://www.ss.lv/msg/lv/transport/cars/mini/paceman/cxgdod.html"))