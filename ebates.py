# Stanley Young
# Ebates - Shopstyle Take Home Assignment
# 8/21/17
# Python 3

import json
import time
import hashlib
from urllib.request import Request, urlopen
from password import secret


# Call API and return JSON obj as dictionary
# API Documentation: http://dev.viki.com/v4/api/
def getPage(page_num, data):
    # create initial url for HMAC-sha1 hashing
    t = str(time.time())[0:10]
    link = 'http://api.viki.io/v4/videos.json?app=100250a&per_page=10&page=' + \
            str(page_num) + '&t=' + t

    h = hashlib.sha1()
    h.update(secret.encode('utf-8'))
    h.update(link.encode('utf-8'))
    sig = h.hexdigest()

    # create final signature & get request
    link = link + '&sig=' + sig
    req = Request(link, headers={'User-Agent':'Mozilla/5.0'})

    page = urlopen(req).read()
    data = json.loads(page.decode('utf-8'))
    return data

# Count the number of hd tags for every page
def count_all(hd_true, hd_false):
    page_num = 1
    data = dict()
    data = getPage(page_num, data)

    while(data['more'] == True):
        for x in range(0, 10): # optimize for any size page
            if data['response'][x]['flags']['hd'] == True:
                hd_true = hd_true + 1
            elif data['response'][x]['flags']['hd'] == False:
                hd_false = hd_false + 1

        page_num += 1
        data = getPage(page_num, data)

    return (hd_true, hd_false)

# Start program
def main():
    hd_true = 0
    hd_false = 0

    hd_true, hd_false = count_all(hd_true, hd_false)
    print("hd-true: %d  hd-false: %d" % (hd_true, hd_false))


if __name__ == '__main__':
    main()
