from __future__ import unicode_literals
import youtube_dl
from time import gmtime, strftime
import urllib2,sys
from BeautifulSoup import BeautifulSoup
import threading
import multiprocessing
from urlparse import urljoin

path = sys.argv[2]

ydl_opts = {'outtmpl': path+strftime("%b %d", gmtime())+'/%(title)s.mp4',
        'cachedir':False}

'''import androidhelper
droid = androidhelper.Android()
mode = droid.dialogGetInput().result'''

mode=sys.argv[1]

def download_video(url,ydl_opts=None):
    print url
    global ydl
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print e

def download_cricingif(ballid):
    start = ballid-6
    for u in range(start,ballid):
        url = "http://www.cricingif.com/Ball/"+str(u)
        print url
        #download_video(url)
        t = threading.Thread(target=download_video, args = (url,))
        #t.daemon = True
        t.start()

def download_cricket(url):
    '''mycrickethighlights.com'''
    url = 'http://mycrickethighlights.com/latest-cricket-highlights/'

    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04"})
    con = urllib2.urlopen(req)
    data=con.read()
    soup = BeautifulSoup(data)

    highlights = soup.findAll('a',{'class':'thumb hasIcon hasVideo'})

    for highlight in highlights:
        url =  urljoin('http://mycrickethighlights.com',highlight.get('href'))

        req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04"})
        con = urllib2.urlopen(req)
        data=con.read()
        soup = BeautifulSoup(data)

        videos = soup.findAll('div', {'class': 'tab-content'})
        for vid in videos:
            iframe = vid.find('iframe')
            iframe = eval(iframe.get('data-id'))
            provider, video_id = iframe[0],iframe[1]
            ydl_opts = {'outtmpl': path+highlight.get('href')+'/%(title)s.mp4',
        'cachedir':False}
            download_video('http://'+provider+".com/video/"+video_id,ydl_opts)

def download_footyroom(file=None):
    global soup, videos, vid, ydl
    url = "http://footyroom.com"
    print url

    if file is None:
        data = urllib2.urlopen(url).read()
    else:
       with open (file, "r") as myfile:
        data=myfile.read()

    soup = BeautifulSoup(data)

    videos = soup.findAll('div', {'class': 'vidthumb'})
    for vid in videos:
        if file is None:

            download_video("http://footyroom.com" + vid.a['href'])
        else:
            print vid.a['href']
            download_video( vid.a['href'])

def download_hootfoot(file=None):
    global soup, videos, vid, ydl
    url = "http://hoofoot.com"
    print url

    if file is None:
        req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"}) 
        con = urllib2.urlopen(req)
        data=con.read()
    else:
       with open (file, "r") as myfile:
            data=myfile.read()

    soup = BeautifulSoup(data)

    videos = soup.findAll('div', {'id': 'port'})
    for vid in videos:
        if file is None:

            download_video("http://hoofoot.com" + vid.a['href'].replace("./?match","/?match"))
        #print vid.a['href']
        else:
            print vid.a['href']
            download_video( vid.a['href'])


#   import ipdb
# ipdb.set_trace()
if(mode == 'ff'):
    download_footyroom("FootyRoom - Football _ Soccer Highlights and Livescores.html")

elif mode == 'f':
        download_footyroom()
elif mode == 'h':
        download_hootfoot()
elif mode =='c':
    url=sys.argv[2]
    # path = sys.argv[3]
    download_cricket(url)
else:
    download_video(mode)

