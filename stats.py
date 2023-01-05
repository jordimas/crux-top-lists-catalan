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

    if netloc.count(".") >= 2:
        first = netloc.index(".") + 1
        second = netloc.index(".", first + 1)
        domain = netloc[first:second]
    else:
        domain = netloc

    return domain, netloc

def main():

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

            url = components[0]
            ranking = components[1]
            lang = components[2].rstrip()


            if lang != "ca":
                continue

            if url in false_positives:
                continue

            domain, netloc = get_domain_and_netloc(url)
            if domain in domains_seen:
#                print(f"Discarding {url} because already seen")
                continue
            else:
                domains_seen.add(domain)

            print(line.rstrip())
            fh_catalan.write(line)

if __name__ == "__main__":
    main()
