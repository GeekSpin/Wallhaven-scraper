########################################################
#        Program to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                                                      #
#                  dated- 26 June 2016                 #
#                 Update - 29 June 2016                #
########################################################

import getpass
import os
import re
import time
from textwrap import dedent

import bs4
import requests
import tqdm

os.makedirs('Wallhaven', exist_ok=True)

def login():
    print('NSFW images require login')
    username = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    req      = requests.post('https://alpha.wallhaven.cc/auth/login',
                                                    data={'username':username,
                                                          'password':password})
    return req.cookies

def choice():
    print('''****************************************************************
                            Category Codes

    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallapapers only.
    ga      - For 'General' and 'Anime' wallapapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ')
    ALL = '111'
    ANIME = '010'
    GENERAL = '100'
    PEOPLE = '001'
    GENERAL_ANIME = '110'
    GENERAL_PEOPLE = '101'
    if ccode.lower() == "all":
        ctag = ALL
    elif ccode.lower() == "anime":
        ctag = ANIME
    elif ccode.lower() == "general":
        ctag = GENERAL
    elif ccode.lower() == "people":
        ctag = PEOPLE
    elif ccode.lower() == "ga":
        ctag = GENERAL_ANIME
    elif ccode.lower() == "gp":
        ctag = GENERAL_PEOPLE

    print('''
    ****************************************************************
                            Purity Codes

    sfw     - For 'Safe For Work'
    sketchy - For 'Sketchy'
    nsfw    - For 'Not Safe For Work'
    ws      - For 'SFW' and 'Sketchy'
    wn      - for 'SFW' and 'NSFW'
    sn      - For 'Sketchy' and 'NSFW'
    all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    pcode = input('Enter Purity: ')
    ptags = {'sfw'     : '100',
             'sketchy' : '010',
             'nsfw'    : '001',
             'ws'      : '110',
             'wn'      : '101',
             'sn'      : '011',
             'all'     : '111'}
    ptag = ptags[pcode]

    if pcode in ['nsfw', 'wn', 'sn', 'all']:
        cookies = login()
    else:
        cookies = dict()

    CATURL = 'https://alpha.wallhaven.cc/search?categories=' + \
                                            ctag + '&purity=' + ptag + '&page='
    return (CATURL, cookies)


def latest():
    print('Downloading latest')
    latesturl = 'https://alpha.wallhaven.cc/latest?page='
    return (latesturl, dict())


def main():
    Choice = input('''Do you want to choose categories or want to download latest wallpapers:
    Enter "yes" for choosing categories
    Enter "no" for Downloading latest wallpapers

    Enter choice: ''')

    if Choice.lower() == 'yes':
        BASEURL, cookies = choice()
    else:
        BASEURL, cookies = latest()

    pgid = int(input('How Many pages you want to Download: '))
    print('Number of Wallpapers to Download: ' + str(24 * pgid))
    for i in range(1, pgid + 1):
        url    = BASEURL + str(i)
        urlreq = requests.get(url, cookies=cookies)
        soup   = bs4.BeautifulSoup(urlreq.text, 'lxml')
        soupid = soup.findAll('a', {'class': 'preview'})
        res    = re.compile(r'\d+')
        imgid  = res.findall(str(soupid))
        imgext = ['jpg', 'png', 'bmp']
        for i in range(len(imgid)):
            url = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven'\
                                                            '-%s.' % imgid[ i]
            for ext in imgext:
                iurl   = url + ext
                imgreq = requests.get(iurl, cookies=cookies)
                if imgreq.status_code == 200:
                    print('Downloading: ' + iurl)
                    with open(os.path.join('Wallhaven',\
                                   os.path.basename(iurl)), 'ab') as imageFile:
                        for chunk in tqdm.tqdm(imgreq.iter_content(1024),\
                                total=(int(imgreq.headers['content-length'])\
                                                           / 1024), unit='KB'):
                            time.sleep(0.01)
                            imageFile.write(chunk)
                break

if __name__ == '__main__':
    main()
