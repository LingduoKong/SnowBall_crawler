import os
import urllib2
import urlparse
import json
from bs4 import BeautifulSoup

page_url = 'http://xueqiu.com'
argument_url = '/statuses/original/timeline.json?user_id=2054435398&_=1451075565174&page='
full_url = urlparse.urljoin(page_url, argument_url)

header = {
    'Host': 'xueqiu.com',
    'Connection': 'keep-alive',
    'cache-control': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Accept-Encoding': 'utf-8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cookie': 's=2e0p1196ea; webp=1; xq_a_token=9d5c52db5d031594dc48856217192de364e69877; xq_r_token=40e47afe96856915b0033e0beded4c340d3ffdb7; __utma=1.500362953.1448083299.1451017699.1451071963.5; __utmc=1; __utmz=1.1451017699.4.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Hm_lvt_1db88642e346389874251b5a1eded6e3=1451017701; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1451071968'
}

# get all urls from user home page and store in the url.txt file

i = 1
new_url_list = open('url.txt', 'w')

while True:
    request = urllib2.Request(full_url + repr(i), headers=header)
    try:
        response = urllib2.urlopen(request)
        j_obj = json.load(response)
        list = j_obj['list']
        if len(list) == 0:
            break
        else:
            i += 1
        for page in list:
            cur_url = urlparse.urljoin(page_url, page['target'])
            new_url_list.write(cur_url + "\n")

    except urllib2.HTTPError, e:
        print e.fp.read()

new_url_list.close()


# create a folder named html and download all html pages from url.txt into html folder

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'utf-8',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

with open('url.txt') as f:
    urls = f.readlines()

dir = 'html'
if not os.path.exists(dir):
    os.mkdir(dir)

for url in urls:
    try:
        request = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(request)
        page = response.read()
        soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
        title = soup.find(class_="status-title").get_text()
        title = title.replace('/', '-')
        print(title)
        file = open('html/' + title, 'w')
        file.write(page)
        file.close()
    except urllib2.HTTPError, e:
        print e.fp.read()



