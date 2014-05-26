#coding:utf-8
"""
Copyright (c) 2014. Kensuke Kousaka

This software is released under the MIT License

http://opensource.org/licenses/mit-license.php
"""
__author__ = 'Kensuke Kousaka'

import time
import httplib2
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run

import key

def main():
    FLOW = OAuth2WebServerFlow(
        client_id=key.client_id,
        client_secret=key.client_secret,
        scope='https://www.googleapis.com/auth/calendar',
        user_agent='CalendarSample/v1'
    )

    storage = Storage('calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = run(FLOW, storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build(serviceName='calendar', version='v3',http=http)
if __name__ == '__main__':
    main()