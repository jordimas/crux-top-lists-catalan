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

    logger.addHandler(console)


def get_false_positives():
    falses = set()
    with open('falsos_positius.txt') as fh:
        for line in fh:
            line = line.strip()
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

domains = {}
    
def _process_group_filter(group, urls, domains_seen, fh_catalan, start_url, end_url):
    processed = []
    len_start_url = len(start_url)
    len_end_url = len(end_url)
    
    for url in urls:

        if start_url and end_url:
            if start_url != url[0:len_start_url] or end_url != url[-len(end_url):]:
                continue

        if start_url:
            if start_url != url[0:len_start_url]:
                continue
                
        if end_url:
            if end_url != url[-len_end_url:]:
                continue                
    
        domain, netloc = get_domain_and_netloc(url)
        if domain in domains_seen:
            logging.debug(f"Discarding {url} because already seen")
            continue
        else:
            domains_seen.add(domain)

        processed.append(url)
        line = f" {url}"
        print(line)
        fh_catalan.write(line + "\n")
        
        global domains
        last = netloc.rfind(".")
        domain = netloc[last+1:]
        count = domains.get(domain)
        if not count:
            count = 1
        else:
            count += 1
            
        domains[domain] = count

    for url in processed:
        urls.remove(url)
        

def process_group(group, urls, domains_seen, fh_catalan):
    line = f"Primers {group} llocs"
    print(line)
    fh_catalan.write(line + "\n")
       
    _process_group_filter(group, urls, domains_seen, fh_catalan, "https://www", ".cat")
    _process_group_filter(group, urls, domains_seen, fh_catalan, "https://www", ".com")
    _process_group_filter(group, urls, domains_seen, fh_catalan, "https://www", ".")
    _process_group_filter(group, urls, domains_seen, fh_catalan, "", ".cat")
    _process_group_filter(group, urls, domains_seen, fh_catalan, "", ".com")        
    _process_group_filter(group, urls, domains_seen, fh_catalan, "", "")
    
def is_false_positive(url, false_positives):
    for false_positive in false_positives:
        if false_positive and false_positive in url:
            return True

    return False

def main():

    init_logging(True)
    URLS_FILE = 'urls.txt'
    total_urls = file_len('data/202211.csv') - 1
    processed =  file_len(URLS_FILE)

    false_positives = get_false_positives()

    domains_seen = set()
    current_group = 0
    current_urls = []
    with open(URLS_FILE) as fh, open('llocs_en_catala.txt', 'w') as fh_catalan:
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

            if is_false_positive(url, false_positives):
                logging.debug(f"Discarding {url} because is a false positive")
                continue

            if redirect_url:
                domain, netloc = get_domain_and_netloc(url)
                redirect_domain, redirect_netloc = get_domain_and_netloc(redirect_url)
                if redirect_domain != domain:
                    logging.debug(f"Discarding because diferent domains: {url} because redirects to {redirect_url}")
                    continue                
                
            if current_group == 0:
                current_group = group

            if current_group != group:
                process_group(current_group, current_urls, domains_seen, fh_catalan)            
                current_group = group
                current_urls.clear()
                            
            current_urls.append(url)
            
        process_group(current_group, current_urls, domains_seen, fh_catalan)
        
        domains_count = "\nNombre d'adreçes per domini de primer nivell: "
        for domain, value in sorted(domains.items(), key=lambda item: item[1], reverse=True):
                domains_count += f"{domain}: {value}, "

        line = domains_count + "\n"
        line += f"Nota: s'han analitzat les primeres {processed} URL de les {total_urls} disponibles"
        print(line)
        fh_catalan.write(line + "\n")

if __name__ == "__main__":
    main()
