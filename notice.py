#!/usr/bin/python3
import os


def send(message):
    event_name = 'iphone_notice'
    key = ''
    data = f'{{\\"value1\\" : \\"{message}\\"}}'
    # print(data)
    os.system(
        f'curl -H "Content-type: application/json" -X POST -d "{data}"  https://maker.ifttt.com/trigger/{event_name}/with/key/{key}')
    print(f'sending IFTTT message: {event_name}')
