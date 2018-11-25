""" scrap 28, for 28 page python scraping
    func:
        getLinks( link ): given a link, then return all the links in this wiki-link.
        
    mainProgram: call getLinks, for the returned links randomlly select one link then call getLinks use this link.
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import datetime



def getLinks(wikiUrl):
    html = urlopen("http://en.wikipedia.org/" + wikiUrl)
    bsObj = BeautifulSoup(html, "html.parser")

    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href = re.compile("^(/wiki/)((?!:).)*"))

links = getLinks("/wiki/Captain_America_(comic_book)")
random.seed(datetime.datetime.now())

while (len(links) > 0):
    newWikiUrl = links[random.randint(0, len(links) - 1)].attrs["href"]
    print (newWikiUrl)
    links = getLinks(newWikiUrl)

