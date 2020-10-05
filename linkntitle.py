import re
import os
import requests
from bs4 import BeautifulSoup

# Scraper function

def ss_linkscrape():
    unique_link_set = list()

    source = requests.get("https://www.ss.lv/lv/transport/cars/infiniti/")
    soup = BeautifulSoup(source.content, "html.parser")
    for link in soup.find_all("a", href=re.compile('/msg/')):
        if 'msg/lv/transport/cars/infiniti/' in link.get('href'):
            link = (link.get('href'))
            link = "http://www.ss.lv{}".format(link)
            if link not in unique_link_set:
                unique_link_set.append(link)

    return unique_link_set


# Header scrape function
def ss_hscrape():
    unique_header_set = list()

    r = requests.get("https://www.ss.lv/lv/transport/cars/infiniti/")
    hdr_dt = BeautifulSoup(r.content, 'lxml')
    for header in hdr_dt.find_all('a', class_="am"):
        extract = header.text.splitlines()
        extract2 = ''.join(extract)
        if extract2 not in unique_header_set:
            unique_header_set.append(extract2)

    return unique_header_set

# Join Link with Header
key_set = ss_linkscrape()
value_set = ss_hscrape()
result = {key_set[i]: value_set[i] for i in range(len(key_set))}
print(result)
