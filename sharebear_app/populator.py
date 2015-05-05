from django.contrib.auth.models import User
from sharebear_app.models import UserProfile, Message
from datetime import datetime
import unicodedata
from faker import Factory
import random
import csv

fake = Factory.create()

def createUsers():
	for i in range(50):
		first_name=fake.first_name()
		last_name=fake.last_name()
			
		user = User.objects.create_user(
			first_name=first_name,
			last_name=last_name,
			email=fake.email(),
			#username=fake.user_name(),
			username="{0}.{1}".format(first_name, last_name),
			password="test123"
			)
		location = fake.city()
		randint = random.randint(0,19)
		profile = UserProfile(user=user, aboutme="Fake data, yo.", location=location, pic='avatars/avatar%s.jpg' % randint)
		profile.save()
		print user, profile
	return True

# def createMessages():
# 	for i in range(1):
# 		meta_message = MetaMessage()
# 		meta_message.save()
# 		message = Message(subject=unicodedata.normalize('NFKD',u' '.join(fake.words(nb=4))).encode('ascii','ignore'),
# 			body=unicodedata.normalize('NFKD',fake.paragraphs(nb=1)[0]).encode('ascii','ignore'),
# 			sender=User.objects.order_by('?')[0],
# 			recipient=User.objects.order_by('?')[0],
# 			meta_msg=meta_message,
# 			sent_at=datetime.now()
# 			)
# 		message.save()
# 		print meta_message, message
# 	return True

# #Define all variables outside of Message class creator and iterate to put in multiple recipients

# def createMultiMessages():

# 	for i in range(1):

# 		meta_message = MetaMessage()
# 		meta_message.save()
		
# 		sender = User.objects.order_by('?')[0]
# 		subject=unicodedata.normalize('NFKD',u' '.join(fake.words(nb=4))).encode('ascii','ignore')
# 		body=unicodedata.normalize('NFKD',fake.paragraphs(nb=1)[0]).encode('ascii','ignore')

# 		for i in range(0,4):
# 			message = Message(subject=subject,
# 				body=body,
# 				sender=sender,
# 				recipient=User.objects.order_by('?')[0],
# 				meta_msg=meta_message,
# 				sent_at=datetime.now()
# 				)
# 			message.save()
# 		print meta_message, message
# 	return True

# def createCSVMessages():
# 	for i in range(100):
# 		meta_message = MetaMessage()
# 		meta_message.save()
# 		sender = User.objects.order_by('?')[0]

# 		with open('./sharebear/musicmessages.csv','rb') as infile:
# 			r = csv.reader(infile)
# 			r.next()
# 			data = [x for x in r]

# 			randint = random.randint(0,11)

# 			subject = data[randint][0]
# 			body = data[randint][1]

# 			for i in range(0,4):
# 				message = Message(subject=subject,
# 					body=body,
# 					sender=sender,
# 					recipient=User.objects.order_by('?')[0],
# 					meta_msg=meta_message,
# 					sent_at=datetime.now()
# 					)
# 				message.save()
# 			print meta_message, message
# 	return True


print createUsers()
#print createCSVMessages()


