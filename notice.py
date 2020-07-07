#!/usr/bin/python3
import os
import requests

# IFTTT APP发送通知函数，注意修改自己的key


def send(message):
    event_name = 'iphone_notice'
    key = ''
    url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/{key}'
    req = requests.post(url, json={"value1": message})
    print(f'sending IFTTT message: {event_name}')
    if req.status_code == 200:
        print('已发送通知')
    else:
        print('error ' + req.status_code)
