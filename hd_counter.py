# Stanley Young
# Ebates - Shopstyle Take Home Assignment
# 8/21/17
# Python 3

import json
import time
import hashlib
from urllib.request import Request, urlopen
# from password import secret
secret = 'PASTE SECRET KEY HERE'

# Check request for valid JSON, store as dictionary
def validJson(page):
    try:
        data = json.loads(page.decode('utf-8'))
        return data
    except ValueError:
        print('Invalid JSON received.')


# Call API and return JSON obj as dictionary
# API Documentation: http://dev.viki.com/v4/api/
def getPage(page_num, data):
    # create initial url for hashing
    t = str(time.time())[0:10]
    link = 'http://api.viki.io/v4/videos.json?app=100250a&per_page=10&page=' + \
            str(page_num) + '&t=' + t

    # HMAC-sha1 hash
    h = hashlib.sha1()
    h.update(secret.encode('utf-8'))
    h.update(link.encode('utf-8'))
    sig = h.hexdigest()

    # create final signature; get and check request
    link = link + '&sig=' + sig
    req = Request(link, headers={'User-Agent':'Mozilla/5.0'})
    page = urlopen(req).read()
    data = validJson(page)

    return data

# Count the number of hd tags for every page
def count_hd(hd_true, hd_false,  page_num, per_page):
    data = dict()
    data = getPage(page_num, data)

    # read pages until the end
    while(data['more'] == True):
        # count true/false in ea page
        for entry in data['response']:
            if entry['flags']['hd'] == True:
                hd_true = hd_true + 1
            elif entry['flags']['hd'] == False:
                hd_false = hd_false + 1

        # get next page
        page_num += 1
        data = getPage(page_num, data)

    return (hd_true, hd_false)

# Start program
def main():
    hd_true = 0
    hd_false = 0
    page_num = 1
    per_page = 10

    hd_true, hd_false = count_hd(hd_true, hd_false, page_num, per_page)
    print("HD-True: %d  HD-False: %d" % (hd_true, hd_false))


if __name__ == '__main__':
    main()
