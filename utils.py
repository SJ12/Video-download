
import urllib2,sys
from BeautifulSoup import BeautifulSoup

def parse_links(url):
    data = urllib2.urlopen(url).read()
    
    soup = BeautifulSoup(data)

    links = soup.findAll('a')
    for link in links:
    	if len(link['href']) > 10: yield link['href'] 

