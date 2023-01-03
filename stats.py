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

def main():

    total_urls = file_len('data/202211.csv') - 1
    processed =  file_len('urls.txt')
    
    false_positives = get_false_positives()
    with open('urls.txt') as fh, open('llocs_en_catala.txt', 'w') as fh_catalan:
        line = f"# Proccesed {processed} of a total of {total_urls}"
        print(line)
        fh_catalan.write(line)
        for line in fh:
            components = line.split(",")

            if len(components) != 3:
                continue
        
            url = components[0]
            ranking = components[1]
            lang = components[2].rstrip()


            if lang != "ca":
                continue

            #print(f"url:'{url}'")
            if url in false_positives:
                continue

            print(line.rstrip())
            fh_catalan.write(line)


   
if __name__ == "__main__":
    main()
