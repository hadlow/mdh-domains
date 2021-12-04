import requests
import re
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()
status, response = http.request('http://www.milliondollarhomepage.com/')

domains = []

f = open("domains.txt", "a")

for link in BeautifulSoup(response, parse_only=SoupStrainer('area')):
    if link.has_attr('href'):
        domain = re.search("^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)", link['href']).group()
        domain = domain.replace("http://", "")
        domain = domain.replace("https://", "")
        domain = domain.replace("www.", "")

        if domain not in domains:
            try:
                r = requests.head(link['href'])
            except requests.ConnectionError:
                domains.append(domain)
                f.write(domain + "\n")
                print(domain)

f.close()
