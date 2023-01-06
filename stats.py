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

from urllib.parse import urlparse
import logging
import os

def init_logging(del_logs):
    logfile = 'stats.log'

    if del_logs and os.path.isfile(logfile):
        os.remove(logfile)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    console = logging.StreamHandler() # By default uses stderr

    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    logger = logging.getLogger('')
    console.setLevel(LOGLEVEL)

    if LOGLEVEL != "INFO":
        console.setFormatter(formatter)

    logger.addHandler(console)


def get_false_positives():
    falses = set()
    with open('falsos_positius.txt') as fh:
        for line in fh:
            line = line.strip()
            #print("**" + line)
            falses.add(line)

    return falses

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def get_domain_and_netloc(url):
    netloc = urlparse(url).netloc

    if netloc.count(".") == 1: # https://twitter.com
        first = 0
        second = netloc.index(".", first + 1)
        domain = netloc[first:second]
    elif netloc.count(".") >= 2:
        first = netloc.index(".") + 1
        second = netloc.index(".", first + 1)
        domain = netloc[first:second]
    else:
        domain = netloc

    return domain, netloc

def main():

    init_logging(True)
    URLS_FILE = 'urls.txt'
    total_urls = file_len('data/202211.csv') - 1
    processed =  file_len(URLS_FILE)

    false_positives = get_false_positives()

    domains_seen = set()
    with open(URLS_FILE) as fh, open('llocs_en_catala.txt', 'w') as fh_catalan:
        line = f"# Proccesed {processed} of a total of {total_urls}"
        print(line)
        fh_catalan.write(line)
        for line in fh:
            components = line.split(",")

            if len(components) != 4:
                continue

            url = components[0].rstrip()
            group = components[1].rstrip()
            lang = components[2].rstrip()
            redirect_url = components[3].rstrip()

            if lang != "ca":
                continue

            if url in false_positives:
                logging.debug(f"Discarding {url} because is a false positive")
                continue

            domain, netloc = get_domain_and_netloc(url)
            if domain in domains_seen:
                logging.debug(f"Discarding {url} because already seen")
                continue
            else:
                domains_seen.add(domain)

            if redirect_url:
                redirect_domain, redirect_netloc = get_domain_and_netloc(redirect_url)
                if redirect_domain != domain:
                    logging.debug(f"Discarding because diferent domains: {url} because redirects to {redirect_url}")
                    continue

            line = f"{url},{group}" 
            print(line)
            fh_catalan.write(line + "\r")

if __name__ == "__main__":
    main()
