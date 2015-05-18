import soundcloud
import csv

def follow():
	client = soundcloud.Client(client_id='0473a0ba44f63d071607ee4d374b4843')
	
#follow()

def followlist():
	with open('soundcloudUserDataHouse.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			print row

	return

followlist()
