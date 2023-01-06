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


from bs4 import BeautifulSoup
import urllib
import urllib.parse
import urllib.request
from langdetect import detect, DetectorFactory
import logging
import os
import threading
from threading import Thread
import datetime
from lingua import Language, LanguageDetectorBuilder

DetectorFactory.seed = 0

def init_logging(del_logs):
    logfile = 'crawler.log'
    logfile_info = 'crawler_info.log'

    if del_logs and os.path.isfile(logfile):
        os.remove(logfile)

    if del_logs and os.path.isfile(logfile_info):
        os.remove(logfile_info)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console = logging.StreamHandler() # By default uses stderr
    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    logger = logging.getLogger('')
    console.setLevel(logging.ERROR)

    logger.addHandler(console)

    fh = logging.FileHandler(logfile_info)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

lock = threading.Lock()

URLS_FILE = "urls.txt"

def _detect_lang(url, text):

    try:

        detector = LanguageDetectorBuilder.from_all_languages().build()

        result = detector.detect_language_of(text)

        if result:
            r =  str(result.iso_code_639_1).lower()
            first = r.index(".") + 1
            return r[first:]

        return result

    except Exception as e:
#        print(f"  Error detecting language for {url}: {e}")
        return None

processed_urls = 0

def _write_file_line(line):
    with lock:
        global processed_urls
        processed_urls += 1
        with open(URLS_FILE, 'a') as file:
            file.write(line + "\n")

def crawl_page(url, group):

    new_url = ""
    try:

        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Accept-Language" : "ca,en-US;q=0.7,en;q=0.3"}

        request = urllib.request.Request(url, headers=headers)
        handle = urllib.request.build_opener()
        op = handle.open(request, timeout=30)
        html = str(
            op.read(),
            'utf-8',
            errors='replace'
        )
        
        final_url = op.geturl()
        if final_url != url:
            logging.info(f"Redirect {url} to {final_url}")
            new_url = final_url

        handle.close()
        soup = BeautifulSoup(html, 'lxml')
        text = soup.text
        words = len(text.split())

        if words > 30:
            language =  detect(soup.text)
            language2 = _detect_lang(url, soup.text[0:min(len(soup.text), 300)])

            if language2:
                new_language = language
                if 'ca'== language and 'ca'!= language2:
                    new_language = language2
                    logging.warning(f"Inconsitant languages detected on {url}: '{language}' - '{language2}'")

                if 'ca'!= language and 'ca'== language2:
                    new_language = language
                    logging.warning(f"Inconsitant languages detected on {url}: '{language}' - '{language2}'")

                language = new_language

        else:
            language = "unknown"

        line = f"{url},{group},{language},{new_url}"
#        print(line)
        logging.debug(f"{url},{group},{language}, {words}")
        _write_file_line(line)

    except Exception as e:
        logging.error(f"Error on {url}: {e}")
        line = f"{url},{group},error,{new_url}"
        _write_file_line(line)

def _get_urls_per_second(start_time, urls):
    time = datetime.datetime.now() - start_time
    total_seconds = time.total_seconds()
    urls_second = urls / total_seconds if total_seconds > 0 else 0
    return urls_second

def main():

    init_logging(True)
    PROTOCOL = "http"
    LEN_PROTOCOL = len(PROTOCOL)

    if os.path.isfile(URLS_FILE):
        os.remove(URLS_FILE)

    urls = 0
    start_time = datetime.datetime.now()
    singleThread = False
    with open('data/202211.csv') as fh:
        threads = []
        for line in fh:
            line = line.rstrip()
            if len(line) < LEN_PROTOCOL or line[0:LEN_PROTOCOL].lower() != PROTOCOL:
                logging.debug(f"skip '{line}'")
                continue

            url, group = line.split(",")

            if singleThread:
                crawl_page(url, group)
            else:
                thread = Thread(target=crawl_page, args=(url, group))
                threads.append(thread)
                thread.start()

                if len(threads) > 50:
                    for thread in threads:
                        thread.join()

                    threads = []

            urls += 1
            if urls % 100 == 0:
                urls_second = _get_urls_per_second(start_time, processed_urls)
                print(f"URLs: {urls}. ULRs per second {urls_second:.1f}")

if __name__ == "__main__":
    main()
