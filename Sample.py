#coding:utf-8
"""
Copyright (c) 2014. Kensuke Kousaka

This software is released under the MIT License

http://opensource.org/licenses/mit-license.php
"""
__author__ = 'Kensuke Kousaka'

import gflags
import httplib2
import codecs
import sys
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run
from apiclient.discovery import build

import key

import datetime


def main(argv):
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	try:
		argv = gflags.FLAGS(argv)
	except gflags.FlagsError, e:
		print ""
		sys.exit()

	storage = Storage('calendar.dat')
	credentials = storage.get()
	if not credentials or credentials.invalid:
		flow = OAuth2WebServerFlow(
			client_id=key.client_id,
			client_secret=key.client_secret,
			scope=['https://www.googleapis.com/auth/calendar'],
			user_agent='API Project/1.0'
		)
		credentials = run(flow, storage)

	http = httplib2.Http()
	credentials.authorize(http)
	service = build('calendar', 'v3', http=http,)

	# Returns entries on the user's calendar list.
	calendars = service.calendarList().list().execute()

	now = datetime.date.today()
	print now

	i = 0

#CommentOut For Test
# パラメータリスト https://developers.google.com/google-apps/calendar/v3/reference/events/list?hl=ja
# singleEventsクエリをTrueにすることで，繰り返しの予定をバラして表示する
	for calendar in calendars['items']:
		events = service.events().list(calendarId=calendar['id'], singleEvents=True, orderBy='startTime').execute()
		print 'Calendar ID is : ' + calendar['summary']
		print calendar['id']

		for event in events['items']:
			print '----------------------------' + str(i) + '-------------------------------------'
			# print 'event :'
			# print event

			print 'summary' in event
			if 'summary' in event:
				print 'event summary : '
				print event['summary']

				eventStart = event['start']
				# print 'eventStart : '
				# print eventStart

				if 'dateTime' in eventStart:
					start = eventStart['dateTime']
					# print 'start : '
					# print start

					startdate = start.split('T')
					print 'start : '
					print startdate[0]
				else:
					start = eventStart['date']
					print 'start : '
					print start

				# start = eventStart['dateTime']
				# print 'start : '
				# print start

				# startdate = start.split('T')
				# print startdate[0]

				eventEnd = event['end']
				# print 'eventEnd : '
				# print eventEnd

				if 'dateTime' in eventEnd:
					end = eventEnd['dateTime']
					# print 'end : '
					# print end

					enddate = end.split('T')
					print 'end : '
					print enddate[0]
				else:
					end = eventEnd['date']
					print 'end : '
					print end

				# end = eventEnd['dateTime']
				# print 'end : '
				# print end
				#
				# enddate = end.split('T')
				# print enddate[0]
				i = i + 1


if __name__ == '__main__':
	main(sys.argv)