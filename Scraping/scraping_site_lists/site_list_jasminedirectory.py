from urllib.request import urlopen
import re
import os
import sys

SITE_URL = 'https://www.jasminedirectory.com/'
TEST_RUN = False
absolute_path = os.path.dirname(__file__)
n = len(sys.argv)

FILE_PATH = os.path.join(absolute_path, '../site_list/jasminedirectory.csv' if n <
                         1 else '../site_list/jasminedirectory_'+sys.argv[1]+'.csv')


alphabet_url_list = list(
    map(lambda x: SITE_URL+'idx,'+chr(x)+'.html', range(97, 123))) if n < 1 else [SITE_URL+'idx,'+sys.argv[1]+'.html']

file = None

if not TEST_RUN:
    file = open(FILE_PATH, 'w+')

for url in alphabet_url_list:
    cat_url_list = []
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    html = html[html.find('<div id="catboxsec">'):html.find('<ul class="alphaIdx">')]
    match_results = re.finditer(
        "<a\s+(?:[^>]*?\s+)?href=([\"'])(.*?)\\1", html, re.IGNORECASE)
    for result in match_results:
        cat_url_list.append(result.group(2))
    i = 0

    if TEST_RUN:
        print('Category urls : '+str(cat_url_list))
    else:
        print('Processing alphabet : '+str(url))

    while (i < len(cat_url_list)):
        page_num = 0
        next_url = None
        url = cat_url_list[i]
        if not TEST_RUN:
            print('Processing category url : '+str(url))
        i += 1
        page_count = 1

        while (page_num < page_count):
            sites = []
            page_URL = SITE_URL + url if page_num == 0 else SITE_URL + \
                url + 'page,' + str(page_num) + '.html'

            if not TEST_RUN:
                print('Processing page url : '+str(page_URL) +
                      ' Page number : '+str(page_num + 1))

            page = urlopen(page_URL)
            inner_html_bytes = page.read()
            inner_html = inner_html_bytes.decode("utf-8")
            if TEST_RUN:
                print('Page Content : ' + inner_html)

            # finding the text in the div tag with class "lnkurl"
            in_match_results = re.finditer(
                '<div class="lnkurl">(.*?)</div>', inner_html, re.IGNORECASE)
            for in_result in in_match_results:
                sites.append(in_result.group(1))
            if not TEST_RUN:
                # writing to file in csv format
                for site in sites:
                    if len(site.strip()) > 0:
                        file.write('"' + site + '",\n')

            if page_num == 0 and inner_html.find('id="catbox"') != -1:
                in_match_results = re.finditer(
                    "<a\s+(?:[^>]*?\s+)?href=([\"'])(.*?)\\1", inner_html[:], re.IGNORECASE)
                for in_result in in_match_results:
                    cat_url_list.append(in_result.group(2))

            # finding the occurrence of the string "pgsel" in the inner html
            if page_num == 0:
                indx = 0
                while indx != -1:
                    indx = inner_html.find('pgsel', indx + 1)
                    if indx != -1:
                        page_count += 1
                    else:
                        page_count -= 2
                print('Page count : '+str(page_count))

            page_num += 1

            if TEST_RUN:
                print('')
                print('After finding sub category urls : ' + str(cat_url_list))
                print('')
                print('Found sites : ' + str(sites))
                break

        if TEST_RUN:
            break

    if TEST_RUN:
        break

if not TEST_RUN:
    file.close()
