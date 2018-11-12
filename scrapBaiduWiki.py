# scrap baidu wiki for poem introduction
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

searchWord = input("input the key word you wanna search:")

session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) \
            AppleWebKit 537.36 (KHTML, like Gecko) Chrome",\
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}


# searchWord = str(searchWord, "utf-8")
wikiUrl = "https://baike.baidu.com/search/none?word="+ searchWord + "&pn=0&rn=10&enc=utf8"

html = session.get(wikiUrl, headers = headers)
if html.encoding == 'ISO-8859-1':
    encodings = requests.utils.get_encodings_from_content(html.text)
    if encodings:
        encoding = encodings[0]
    else:
        encoding = html.apparent_encoding
    global encode_content
    encode_content = html.content.decode(encoding, 'replace')
 
# this html return binary file, but beautifulsoup need text, so return html.text
# html = urlopen(wikiUrl)
bsObj = BeautifulSoup(encode_content, "html.parser")
nextLink = bsObj.find("a", {"class":"result-title"})

contentUrl = session.get(nextLink.attrs["href"], headers = headers)
if contentUrl.encoding == 'ISO-8859-1':
    encodings = requests.utils.get_encodings_from_content(contentUrl.text)
    if encodings:
        encoding = encodings[0]
    else:
        encoding = contentUrl.apparent_encoding
    encode_content = contentUrl.content.decode(encoding, 'replace') 


bsObjN = BeautifulSoup(encode_content, "html.parser")
# print(bsObjN)
content = bsObjN.find("meta", {"name": "description"})
print (content.attrs["content"])
