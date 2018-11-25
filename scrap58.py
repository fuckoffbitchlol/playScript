"""
goal: 
    1. get edit ip from wikipedia page
    2. use API to locate ip

need:
    1. get and read the html file --- urlopen / bs4
    2. get the editor ip from html --- re / bs4
    3. from ip get location --- API

future: maybe we can make a map of wikipedia editor (even though I cant see the meaning)
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
import json

random.seed(datetime)

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*"))

def getHistoryIPs(pageUrl):
    # the format of editor history ip
    # http://en.wikipedia.org/w/index.php?title=[title_in_url]&action=history
    # pageUrl format is like
    # /wiki/Captain_America_(comic_book)
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title=" + pageUrl + "&action=history"

    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    # find the link whose class attribute is "mw-anonuserlink"
    ipAddress = bsObj.findAll("a", {"class": "mw-anonuserlink"})
    addressSet = set()
    for ipAdd in ipAddress:
        addressSet.add(ipAdd.get_text())
    return addressSet


links = getLinks("/wiki/Captain_America_(comic_book)")

while(len(links) > 0):
    selectLink = random.randint(0, len(links))
    for link in links:
        historyIPs = getHistoryIPs(link.attrs["href"])
        print ("current link is:" + link)
        for historyIP in historyIPs:
            print(historyIP)

    newUrl = links[random.randint(0, len(links))].attrs["href"]
    links = getLinks(newUrl)

def getCountry(ipAdress):
    try:
        # what is the read() and decode utf-8 for ???
        response = urlopen("http://freegeoip.net/json/" + ipAdress).read().decode("utf-8")
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get("country_code")



