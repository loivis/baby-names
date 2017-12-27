#!/usr/bin/env python3

import random
import sys
import time

import requests
from bs4 import BeautifulSoup as bs

tid = sys.argv[1]
tianya = 'http://bbs.tianya.cn'
path = tianya + '/post-funinfo-{}-1.shtml'.format(tid)
output = tid + '.html'
headers = {
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
host = ''

with open(output, 'w') as file:
    file.write('')

while True:
    print(path)
    page = requests.get(path, headers=headers)
    soup = bs(page.text, 'html.parser')
    page_number = soup.find('div', {'class': 'atl-pages'}).find('strong').text
    # check host
    if not host:
        post_head = soup.find('div', id='post_head')
        title = post_head.find('span', {'class': 's_title'}).find('span').text
        host = post_head.find('div', {'class': 'atl-info'}).find('a')['uname']
        print('set host to:', host)
        with open(output, 'w') as file:
            file.write('<h1>{}</h1>'.format(title))
    with open(output, 'a') as file:
        file.write(
            '<h2><a href="{0}" target="_blank">{0}</a></h2>'.format(path))
    # parse posts
    posts = soup.find_all('div', attrs={'_host': host})
    for post in posts:
        head = '\n<p style="color:blue"><b>Page {} | {} | {}</b></p>\n'.format(
            page_number, host, post['js_restime'])
        content = post.find('div', attrs={'class': 'bbs-content'})
        imgs = content.find_all('img')
        if imgs:
            for img in imgs:
                img.decompose()
        with open(output, 'a') as file:
            file.write(head)
            file.write(str(content).replace('\t', ''))
    # procceed to next page
    next_page = soup.find('a', attrs={'class': 'js-keyboard-next'})
    if not next_page:
        break
    path = tianya + next_page['href']
    time.sleep(random.randint(5, 10))
