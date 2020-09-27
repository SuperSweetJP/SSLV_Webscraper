import re
import os
import requests
from bs4 import BeautifulSoup

# Scraper function


def ss_scrape(page_link):
    unique_link_set = list()

    source = requests.get("https://www.ss.lv/lv/transport/cars/alfa-romeo/" + str(page_link))
    soup = BeautifulSoup(source.content, "html.parser")
    for link in soup.find_all("a", href=re.compile('/msg/')):
        if 'msg/lv/transport/cars/alfa-romeo/' in link.get('href'):
            link = (link.get('href'))
            link = "http://www.ss.lv{}".format(link)
            if link not in unique_link_set:
                unique_link_set.append(link)

    return "\n".join(unique_link_set) + "\n"

# Page loop list


p_link = ["", "page2.html", "page3.html", "page4.html", "page5.html"]
page_c = 0
while page_c != 4:
    ss_scrape(p_link[page_c])
    # Write links to file
    linklist = open("linklist.txt", "a")
    linklist.write(ss_scrape(p_link[page_c]))
    linklist.close()
    page_c += 1
    if page_c == 4:
        break

# Filter duplicates out duplicates to new file
lines_seen = set()
with open("linklistsort.txt", "w") as output_file:
    for each_line in open("linklist.txt", "r"):
        if each_line not in lines_seen:
            output_file.write(each_line)
            lines_seen.add(each_line)

# Remove clutter file
if os.path.exists("linklist.txt"):
    os.remove("linklist.txt")


# Testing Testing 1 2 3