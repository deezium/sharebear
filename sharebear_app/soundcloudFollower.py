import soundcloud
import time
import csv

def follow():
	client = soundcloud.Client(access_token='1-129923-153597934-f5c1015d92336')
	with open('soundcloudUserDataAllUnique.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')

		userlist = [row[4] for row in reader]

		#print tracklist, len(tracklist)

		csvfile.close()

	for u in userlist[:30]:
		try:
			client.put('/me/followings/%s' % u)
			time.sleep(3)
			print u +  ' followed'
		except:
			pass

	return

def like():
	client = soundcloud.Client(access_token='1-129923-153597934-f5c1015d92336')
	with open('soundcloudUserDataAllUnique.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')

		tracklist = [row[0] for row in reader]

		#print tracklist, len(tracklist)

		csvfile.close()

	for t in tracklist[:30]:
		try:
			client.put('/me/favorites/%s' % t)
			time.sleep(3)
			print t +  ' favorited'
		except:
			pass

	return

	#client.put('/me/favorites/%d' % 115372676)


def csvUniquer():
	with open('soundcloudUserDataAll.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')

		id_list = []
		writer_list = []

		for row in reader:
			user_id = row[4]
			if user_id not in id_list:
				id_list.append(user_id)
				writer_list.append(row)
		csvfile.close()

	print len(id_list)
	print len(writer_list)

	with open('soundcloudUserDataAllUnique.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		for row in writer_list:
			writer.writerow(row)
	
		csvfile.close()

	return
	
def followlist():
	with open('soundcloudUserDataAllUnique.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		
		follow_list = []
		for row in reader:
			print row[4]
			follow_list.append(row[4])

		csvfile.close()

	print len(follow_list)
	follow_set = list(set(follow_list))
	print len(follow_set)
	return follow_set


def likelist():
	with open('soundcloudUserDataAllUnique.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		
		like_list = []
		for row in reader:
			print row[0]
			like_list.append(row[0])
		csvfile.close()

	print len(like_list)
	like_set = list(set(like_list))
	print len(like_set)
	return like_set

#like()
follow()
