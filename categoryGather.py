import re
import os
import requests
from bs4 import BeautifulSoup

#hard coded category for now
#ToDo rework into main loop that passes all categories later on
categoryLink="https://www.ss.lv/lv/transport/cars/fiat/"

#ToDo refractor into db
def scrapeListPage(page_link):
    unique_link_set = list()

    source = requests.get("https://www.ss.lv/lv/transport/cars/alfa-romeo/" + str(page_link))
    soup = BeautifulSoup(source.content, "html.parser")
    for link in soup.find_all("a", href=re.compile('/msg/')):
        if 'msg/lv/transport/cars/alfa-romeo/' in link.get('href'):
            link = (link.get('href'))
            link = "http://www.ss.lv{}".format(link)
            if link not in unique_link_set:
                unique_link_set.append(link)
    
    return unique_link_set

# Page loop list
def categoryLoop(catLink):
    #screape the original page
    scrapeListPage(catLink)
    i = 2
    #scrape subsequent pages, break when return to original page
    while True:
        catLinkNextPage = catLink + "page" + str(i) + ".html"
        nextPageReq = requests.get(catLinkNextPage)
        if catLink == nextPageReq.url:
            break
        scrapeListPage(catLinkNextPage)
        i += 1

    #p_link = ["", "page2.html", "page3.html", "page4.html", "page5.html"]
    #page_c = 0
    #while page_c != 4:
    #    scrapeListPage(p_link[page_c])
    #    # Write links to file
    #    linklist = open("linklist.txt", "a")
    #    linklist.write(scrapeListPage(p_link[page_c]))
    #    linklist.close()
    #    page_c += 1
    #    if page_c == 4:
    #        break

categoryLoop(categoryLink)

# Filter duplicates out duplicates to new file
#TODO save links to db
#ToDo implement check for existing, changed, removed
#lines_seen = set()
#with open("linklistsort.txt", "w") as output_file:
#    for each_line in open("linklist.txt", "r"):
#        if each_line not in lines_seen:
#            output_file.write(each_line)
#            lines_seen.add(each_line)

## Remove clutter file
#if os.path.exists("linklist.txt"):
#    os.remove("linklist.txt")
