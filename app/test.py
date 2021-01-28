#!/usr/bin/python3

from scanner import Scanner

s = Scanner('55.35.4.0/24')
r = s.scan_network()


for h in r:
    for p in h:
        if p['status'] == 'OPEN':
            print(f'{p["host"]} is listening on {p["port"]}')
