import soundcloud
import urllib2
import json
import csv

def finder():
	client = soundcloud.Client(client_id='0473a0ba44f63d071607ee4d374b4843')
	# tracks = client.get('/tracks', q='rihanna', bpm={'from': 120})
	# for t in tracks:
	# 	print t.title

	users = client.get('/users', q='Berlin')
	for u in users:
		print u.id, u.full_name, u.online, u.followers_count


#finder()

def curler(url):
	response = urllib2.urlopen(url)
	data = json.load(response)
	data.keys()
	# values = data.values()
	# ouptut_list = [x for x in values]
	#first_name = data['full_name']
	#last_name = data['last_name']
	#username = data['username']
	followers = data['followers_count']
	permalink_url = data['permalink_url']

	ouptut_list = [followers, permalink_url]

	return ouptut_list


def trackSearch():

	result_size = 200
	client = soundcloud.Client(client_id='0473a0ba44f63d071607ee4d374b4843')
	
	#tracks = client.get('/tracks', genres='trap', limit=result_size)
	
	tracks = client.get('/tracks', genres='hardstyle', limit=result_size)

	csvRows = [[t.id, t.permalink_url, t.created_at, t.genre, t.user_id, t.user['permalink_url']] for t in tracks]

	data = client.get('/tracks', genres='hardstyle', limit=result_size, linked_partitioning=1)
	url = data.next_href
	#print tracks.next_href
	i = 0

	for i in range(10):
		print url

		try:
			response = urllib2.urlopen(url)

			data = json.load(response)

			for i in range(len(data['collection'])):
				newRow = [data['collection'][i]['id'], data['collection'][i]['permalink_url'], data['collection'][i]['created_at'], data['collection'][i]['genre'], data['collection'][i]['user_id'], data['collection'][i]['user']['permalink_url']]
				csvRows.append(newRow)
			url = data['next_href']

			print len(csvRows)
		except:
			print "fuck"

	return csvRows

#print trackSearch()


def followerGetter():

	csvRows = trackSearch()
	for i in range(len(csvRows)):
		try:
			user_id = csvRows[i][4]
			url = 'http://api.soundcloud.com/users/'+ str(user_id) + '.json?client_id=ebd558f0b96aa8f07026aa2fe3be5fd8'
			response = urllib2.urlopen(url)
			data = json.load(response)

			followers = data['followers_count']
			csvRows[i].append(followers)
			print csvRows[i]
		except:
			pass

	return csvRows

#print followerGetter()

def writeCSV(outputfile):
	data = followerGetter()
	header = ['track_id', 'track_permalink', 'track_created', 'track_genre', 'creator_id', 'creator_permalink', 'creator_followers']
	with open(outputfile,'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(header)
		for row in data:
			try:
				writer.writerow(row)
			except:
				pass

		csvfile.close()

	print "Success!"
	return

#trackSearch()

#print curler('http://api.soundcloud.com/users/3208.json?client_id=ebd558f0b96aa8f07026aa2fe3be5fd8')
writeCSV('soundcloudUserDataHardstyle.csv')