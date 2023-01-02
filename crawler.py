#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2023 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from bs4 import BeautifulSoup
import urllib
import urllib.parse
import urllib.request
from langdetect import detect
import logging
import os
import threading

from urllib.request import Request, urlopen
from urllib.error import HTTPError

def init_logging(del_logs):
    logfile = 'crawler.log'
    logfile_error = 'crawler-error.log'

    if del_logs and os.path.isfile(logfile):
        os.remove(logfile)

    if del_logs and os.path.isfile(logfile_error):
        os.remove(logfile_error)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    console = logging.StreamHandler() # By default uses stderr

    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    logger = logging.getLogger('')
    console.setLevel(LOGLEVEL)

    if LOGLEVEL != "INFO":
        console.setFormatter(formatter)

    logger.addHandler(console)

    fh = logging.FileHandler(logfile_error)
    fh.setLevel(logging.ERROR)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

lock = threading.Lock()

URLS_FILE = "urls.txt"

def crawl_page(url, group):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
#                   "Accept-Language" : "ca,en-US;q=0.7,en;q=0.3"}
                   
        request = urllib.request.Request(url, headers=headers)
        handle = urllib.request.build_opener()
        html = str(
            handle.open(request, timeout=10).read(),
            'utf-8',
            errors='replace'
        )
        
        handle.close()
        soup = BeautifulSoup(html, 'lxml')
        language =  detect(soup.text)
        line = f"--{url},{group},{language}"       
#        print(line)
        with lock:
	        with open(URLS_FILE, 'a') as file:
		        file.write(line + "\n")

    except Exception as e:
        logging.error(f"Error on {url}: {e}")

        with lock:
            with open(URLS_FILE, 'a') as file:
                line = f"--{url}, error"
                file.write(line + "\n")

def main():
    
    init_logging(True)
    PROTOCOL = "http"
    LEN_PROTOCOL = len(PROTOCOL)
    cnt = 0
    
    if os.path.isfile(URLS_FILE):
        os.remove(URLS_FILE)
        
    with open('data/202211.csv') as fh, ThreadPoolExecutor(max_workers=5) as executor:
        for line in fh:
            line = line.rstrip()
            if len(line) < LEN_PROTOCOL or line[0:LEN_PROTOCOL].lower() != PROTOCOL:
                logging.debug(f"skip '{line}'")
                continue

            url, group = line.split(",")
#            executor.submit(crawl_page, url, group)
#            print(cnt)
            crawl_page(url, group)
            cnt += 1
            if cnt % 1000 == 0:
                print(f"Processed {cnt} lines")
            
#            if cnt > 1000:
#                break

if __name__ == "__main__":
    main()
