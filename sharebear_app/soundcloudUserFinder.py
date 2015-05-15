import soundcloud

def finder():
	client = soundcloud.Client(client_id='0dade5038dabd4be328a885dde4d5e0e')
	tracks = client.get('/tracks', q='buskers', license='cc-by-sa')
	users = client.get('/users', followers_count=100)
	for u in users:
		print u.followers_count

	# for t in tracks:
	# 	print t.title

finder()