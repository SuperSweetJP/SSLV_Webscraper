import requests
from bs4 import BeautifulSoup

# Infiniti single link variable extraction test


def ss_scrapevars():

    vari_set = list()

    # Source scrape

    r = requests.get("https://www.ss.lv/msg/lv/transport/cars/infiniti/fx/acpnl.html")
    soup = BeautifulSoup(r.content, "html.parser")

    # Get Basic Data

    for getmakemodel in soup.find_all('table', class_='options_list'):
        for makemodel in getmakemodel.find_all('td', class_='ads_opt'):
            alldata = makemodel.text
            if alldata not in vari_set:
                vari_set.append(alldata)

    vari_set.pop(10)
    vari_set.pop(9)
    vari_set.pop(7)
    # print(vari_set)

    ckey_set = ("mnf", "yr", "engi", "gbox", "mlg", "clr", "bdy", "svc")
    dtkey = {ckey_set[i]: vari_set[i] for i in range(len(ckey_set))}

    # Test print keyset
    print(dtkey)
    print("\n-------------------------\n")

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

    # Test print variables
    print(marka)
    print(gads)
    print(motors)
    print(karba)
    print(nobr)
    print(krasa)
    print(virsb)
    print(apskate)


ss_scrapevars()
