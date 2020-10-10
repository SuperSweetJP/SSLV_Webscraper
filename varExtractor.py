import requests
from bs4 import BeautifulSoup

# Infiniti single link variable extraction test


def ss_scrapevars():

    vari_set = list()
    equip_set = list()

    # Source scrape

    r = requests.get("https://www.ss.lv/msg/lv/transport/cars/uaz/3741/okjck.html")
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
    vari_set.pop(7)
    print(vari_set)

    ckey_set = ("mnf", "yr", "engi", "gbox", "mlg", "clr", "bdy", "svc")
    dtkey = {ckey_set[i]: vari_set[i] for i in range(len(ckey_set))}

    # Test print keyset
    print(dtkey)
    print("\n-------------------------\n")

    for equipment in soup.find_all('b', class_='auto_c'):
        equipped = equipment.text
        if equipped not in equip_set:
            equip_set.append(equipped)

    # variables:
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

    # Test print variables
    print(marka)
    print(gads)
    print(motors)
    print(karba)
    print(nobr)
    print(krasa)
    print(virsb)
    print(apskate)
    print('\n-------------------\n')
    print(apriko)


ss_scrapevars()
