from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from collections import OrderedDict
from sharebear_app.forms import AuthenticateForm, UserCreateForm, EditProfileForm, ComposeForm, MessageLikeForm, UsernameEditForm, FeaturedEntryForm
from sharebear_app.models import UserProfile, Message, MessageLike, Relationship, SpreadMessage, TrackPlay, FeaturedEntry
from sharebear_app.utils import get_user_model, get_username_field, epoch_seconds, hot
from urllib2 import urlopen
from operator import itemgetter
import json
import re
import urlparse
import soundcloud

User = get_user_model()

def index(request, auth_form=None, user_form=None):
	entry = FeaturedEntry.objects.last()
	print entry
	return render(request, 'featured.html', {'entry': entry, })
	# if request.user.is_authenticated():
	# 	user = request.user
	# 	return redirect('/feed/')
	# else:
	# 	auth_form = auth_form or AuthenticateForm()
	# 	user_form = user_form or UserCreateForm()
	# 	return redirect('/all/')

def login_view(request):
	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return redirect('/feed/')
		else:
			return index(request, auth_form=form)
	return redirect('/')

def logout_view(request):
	logout(request)
	return redirect('/')

def signup(request):
	if request.method == 'POST':
		user_form = UserCreateForm(data=request.POST)
		if user_form.is_valid():
			username = user_form.clean_username()
			password = user_form.clean_password2()
			user_form.save()
			user = authenticate(username=username, password=password)
			login(request, user)

			meta_messages = MetaMessage.objects.order_by('?')[:5]

			messages = [m.sub_messages.first() for m in meta_messages]

			print meta_messages
			print messages

			for msg in messages:
				Message.objects.create(sender=msg.sender, recipient=request.user, subject=msg.subject, body=msg.body, sent_at=timezone.now())

			return redirect('/inbox/')
		else:
			return index(request, user_form=user_form)
	return redirect('/')

def edit_profile(request):
	try: 
		profile=UserProfile.objects.get(user=request.user)
	except:
		pass
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=profile)
		form.user = request.user
		next_url = request.POST.get('next_url', '/')
		if form.is_valid():
			form.save()
			return redirect(next_url)
	return redirect('/')

def edit_username(request):
	try:
		user = request.user
	except:
		pass
	if request.method == 'POST':
		form = UsernameEditForm(request.POST, instance=user)
		form.user = request.user
		next_url_feed = request.POST.get('next_url_feed', '/')
		if form.is_valid():
			form.save()
			return redirect(next_url_feed)
	return redirect('/')

def get_latest(user):
	try:
		return user.visit_set.order_by('-id')[0]
	except IndexError:
		return ""

def users(request, username="", edit_form=None):
	following=False
	if username:
		try:
			profile_user = User.objects.get(username=username)
			userprofile = UserProfile.objects.get_or_create(user=profile_user)
		except User.DoesNotExist:
			raise Http404
		try:
			user = request.user
			if profile_user == request.user:
				edit_form = EditProfileForm(initial={'location': user.profile.location, 'aboutme':user.profile.aboutme, })
			if user.profile.is_following(userprofile[0]):
				following=True
		except:
			pass

		full_message_list = profile_user.sent_messages.all()

		view_count_list = []
		prop_count_list = []
		full_youtube_list = []
		full_soundcloud_list = []

		client = soundcloud.Client(client_id='0dade5038dabd4be328a885dde4d5e0e')

		for message in full_message_list:
			youtube_id = None
			soundcloud_info = ''
			view_count = message.message_spreadmessages.all().count() + profile_user.profile.get_followers().count()
			prop_count = message.message_likes.filter(ever_liked=1).count()

			view_count_list.append(view_count)
			prop_count_list.append(prop_count)
		
			if re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body):
				youtube_s = re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body).group(0)
				youtube_string = "http://"+youtube_s

				url_data = urlparse.urlparse(youtube_string)
				query = urlparse.parse_qs(url_data.query)
				youtube_id = query["v"][0]
			full_youtube_list.append(youtube_id)

			if re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body):
				soundcloud_s = re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body).group(0)
				track_url = "https://"+soundcloud_s

				embed_info = client.get('/oembed', url=track_url)

				old_soundcloud_info = embed_info.html

				old_soundcloud_info = old_soundcloud_info[:-10]

				soundcloud_info = old_soundcloud_info + " class='iframeplayer' m='"+ str(message.id) +"'></iframe>"

				print soundcloud_info

			full_soundcloud_list.append(soundcloud_info)


		#print full_youtube_list

		parameter_list = [[full_message_list[i], full_youtube_list[i], full_soundcloud_list[i], view_count_list[i], prop_count_list[i]] for i in range(len(full_youtube_list))]
		#print parameter_list

		#feed_message_list = [[i, i.is_liked_by_user(user), 1] for i in full_message_list]
		# print feed_message_list

		share_message_list = []
		try:
			user = request.user

			for i in parameter_list:
				share_message_list.append([i[0],i[0].is_liked_by_user(user),i[0].ever_liked_by_user(user),i[1],i[2],i[3],i[4]])
		except:
			for i in parameter_list:
				share_message_list.append([i[0],1,1,i[1],i[2],i[3],i[4]])
		like_form=MessageLikeForm()

		return render(request, 'profile.html', {'next_url': '/users/%s' % user.username, 'profile_user': profile_user, 'user': user, 'userprofile': userprofile, 'edit_form': edit_form, 'following': following, 'share_message_list': share_message_list, 'like_form': like_form, })
	users = User.objects.all()
	return redirect('/')

def likes(request, username="", edit_form=None):
	user = request.user
	following=False
	if username:
		try:
			profile_user = User.objects.get(username=username)
			userprofile = UserProfile.objects.get_or_create(user=profile_user)
		except User.DoesNotExist:
			raise Http404
		try:
			user = request.user
			if profile_user == request.user:
				edit_form = EditProfileForm(initial={'location': user.profile.location, 'aboutme':user.profile.aboutme, })
			if user.profile.is_following(userprofile[0]):
				following=True
		except:
			pass

		message_likes_list = profile_user.user_likes.filter(is_liked=True).order_by('-liked_at')

		full_message_list = [f.msg for f in message_likes_list]

		view_count_list = []
		prop_count_list = []
		full_youtube_list = []
		full_soundcloud_list = []

		client = soundcloud.Client(client_id='0dade5038dabd4be328a885dde4d5e0e')

		for message in full_message_list:
			youtube_id = None
			soundcloud_info = ''
			view_count = message.message_spreadmessages.all().count() + profile_user.profile.get_followers().count()
			prop_count = message.message_likes.filter(ever_liked=1).count()

			view_count_list.append(view_count)
			prop_count_list.append(prop_count)
		
			if re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body):
				youtube_s = re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body).group(0)
				youtube_string = "http://"+youtube_s

				url_data = urlparse.urlparse(youtube_string)
				query = urlparse.parse_qs(url_data.query)
				youtube_id = query["v"][0]
			full_youtube_list.append(youtube_id)

			if re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body):
				soundcloud_s = re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body).group(0)
				track_url = "https://"+soundcloud_s

				embed_info = client.get('/oembed', url=track_url)

				old_soundcloud_info = embed_info.html

				old_soundcloud_info = old_soundcloud_info[:-10]

				soundcloud_info = old_soundcloud_info + " class='iframeplayer' m='"+ str(message.id) +"'></iframe>"

				print soundcloud_info

			full_soundcloud_list.append(soundcloud_info)

		#print full_youtube_list

		parameter_list = [[full_message_list[i], full_youtube_list[i], full_soundcloud_list[i], view_count_list[i], prop_count_list[i]] for i in range(len(full_youtube_list))]
		#print parameter_list

		#feed_message_list = [[i, i.is_liked_by_user(user), 1] for i in full_message_list]
		# print feed_message_list

		share_message_list = []
		try:
			user = request.user
			for i in parameter_list:
				share_message_list.append([i[0],i[0].is_liked_by_user(user),i[0].ever_liked_by_user(user),i[1],i[2],i[3],i[4]])
		except:
			for i in parameter_list:
				share_message_list.append([i[0],1,1,i[1],i[2],i[3],i[4]])

		like_form=MessageLikeForm()

		return render(request, 'likes.html', {'next_url': '/users/%s' % user.username, 'profile_user': profile_user, 'user': user, 'userprofile': userprofile, 'following': following, 'share_message_list': share_message_list, 'like_form': like_form, })
	users = User.objects.all()
	return redirect('/')

def shares(request, username="", compose_form=ComposeForm, success_url=None):
	user = request.user
	profile_user = User.objects.get(username=username)

	if user == profile_user:
		#message_list = Message.objects.feed_for(request.user)
		full_message_list = profile_user.sent_messages.all()

		view_count_list = []
		play_count_list = []
		prop_count_list = []
		full_youtube_list = []
		full_soundcloud_list = []

		client = soundcloud.Client(client_id='0dade5038dabd4be328a885dde4d5e0e')

		for message in full_message_list:
			youtube_id = None
			soundcloud_info = ''

			view_count = message.message_spreadmessages.all().count() + profile_user.profile.get_followers().count()
			prop_count = message.message_likes.filter(ever_liked=1).count()
			play_count = message.message_track_plays.all().count()

			view_count_list.append(view_count)
			prop_count_list.append(prop_count)
			play_count_list.append(play_count)
		
			if re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body):
				youtube_s = re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body).group(0)
				youtube_string = "http://"+youtube_s

				url_data = urlparse.urlparse(youtube_string)
				query = urlparse.parse_qs(url_data.query)
				youtube_id = query["v"][0]
			full_youtube_list.append(youtube_id)

			if re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body):
				soundcloud_s = re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body).group(0)
				track_url = "https://"+soundcloud_s

				embed_info = client.get('/oembed', url=track_url)

				soundcloud_info = embed_info.html

			full_soundcloud_list.append(soundcloud_info)

		print user.profile.get_likes()
		

		#print full_youtube_list

		parameter_list = [[full_message_list[i], full_youtube_list[i], full_soundcloud_list[i], view_count_list[i], play_count_list[i], prop_count_list[i]] for i in range(len(full_youtube_list))]
		#print parameter_list

		#feed_message_list = [[i, i.is_liked_by_user(user), 1] for i in full_message_list]
		# print feed_message_list

		share_message_list = []
		for i in parameter_list:
			share_message_list.append([i[0],i[0].is_liked_by_user(user),i[0].ever_liked_by_user(user),i[1],i[2],i[3],i[4],i[5]])
		
		like_form=MessageLikeForm()

		if request.method == "POST":
			user = request.user
			compose_form = compose_form(data=request.POST)

			recipient_list = User.objects.order_by('?')[:12]

			print recipient_list

			if compose_form.is_valid():
				f = compose_form.save(commit=False)
				f.creator = request.user
				f.creation_time = timezone.now()
				f.save()
				print f

				for i in range(len(recipient_list)):
					new_spread_message = SpreadMessage(user=recipient_list[i],msg=f)
					new_spread_message.save()
				messages.info(request, u"Message successfully sent.")
				if success_url is None:
					success_url = reverse('messages_recipients', kwargs={'message_id': f.id})
					#success_url = reverse('messages_recipients', kwargs={'meta_message_id': m.id})
				if 'next' in request.GET:
					success_url = request.GET['next']
				if 'next' in request.POST:
					success_url = request.POST['next']
				return HttpResponseRedirect(success_url)

		return render(request, 'shares.html', {'share_message_list': share_message_list, 'user': user, 'profile_user': profile_user, 'like_form': like_form, 'compose_form': compose_form, })
	else:
		return redirect('/')

def edit(request, username="", edit_form=None):
	user = request.user
	following=False
	if username:
		try:
			profile_user = User.objects.get(username=username)
			userprofile = UserProfile.objects.get_or_create(user=profile_user)
		except User.DoesNotExist:
			raise Http404
		if profile_user == request.user:
			edit_form = EditProfileForm(initial={'location': user.profile.location, 'aboutme':user.profile.aboutme, })
			username_form = UsernameEditForm(initial={'username': user.username, })
		if user.profile.is_following(userprofile[0]):
			following=True
		return render(request, 'edit.html', {'next_url': '/users/%s' % user.username, 'next_url_feed': '/feed/', 'profile_user': profile_user, 'user': user, 'userprofile': userprofile, 'edit_form': edit_form, 'username_form': username_form, 'following': following, })
	users = User.objects.all()
	return redirect('/')

	#return render(request, 'users.html', {'users': users, 'username': request.user.username, })

@login_required
def feed(request, like_form=None, compose_form=ComposeForm, success_url=None):
	user = request.user
	#message_list = Message.objects.feed_for(request.user)
	spread_list = SpreadMessage.objects.filter(user=request.user)
	
	followed_users = user.profile.get_following()
	spread_message_list = [x.msg for x in spread_list]
	
	followed_message_list = [x.user.sent_messages.all() for x in followed_users]

	flattened_followed_message_list = [item for sublist in followed_message_list for item in sublist]

	full_message_list_duped = spread_message_list + flattened_followed_message_list

	full_message_set = set(full_message_list_duped)

	full_message_list = list(full_message_set)

	full_message_list.sort(key=lambda m: m.creation_time, reverse=True)

	full_youtube_list = []
	full_soundcloud_list = []

	client = soundcloud.Client(client_id='0dade5038dabd4be328a885dde4d5e0e')

	for message in full_message_list:
		youtube_id = None
		soundcloud_info = ''
		if re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body):
			youtube_s = re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body).group(0)
			youtube_string = "http://"+youtube_s

			url_data = urlparse.urlparse(youtube_string)
			query = urlparse.parse_qs(url_data.query)
			youtube_id = query["v"][0]
		full_youtube_list.append(youtube_id)

		if re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body):
			soundcloud_s = re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body).group(0)
			track_url = "https://"+soundcloud_s

			embed_info = client.get('/oembed', url=track_url)

			old_soundcloud_info = embed_info.html

			old_soundcloud_info = old_soundcloud_info[:-10]

			soundcloud_info = old_soundcloud_info + " class='iframeplayer' m='"+ str(message.id) +"'></iframe>"

		full_soundcloud_list.append(soundcloud_info)

	parameter_list = [[full_message_list[i], full_youtube_list[i], full_soundcloud_list[i]] for i in range(len(full_youtube_list))]

	feed_message_list = []
	for i in parameter_list:
		feed_message_list.append([i[0],i[0].is_liked_by_user(user),i[0].ever_liked_by_user(user),i[1],i[2]])

	#print feed_message_list

	like_form=MessageLikeForm()

	if request.method == "POST":
		user = request.user
		compose_form = compose_form(data=request.POST)

		recipient_list = User.objects.order_by('?')[:12]

		#print recipient_list

		if compose_form.is_valid():
			f = compose_form.save(commit=False)
			f.creator = request.user
			f.creation_time = timezone.now()
			f.save()
			print f

			for i in range(len(recipient_list)):
				new_spread_message = SpreadMessage(user=recipient_list[i],msg=f)
				new_spread_message.save()
			messages.info(request, u"Message successfully sent.")
			if success_url is None:
				success_url = reverse('messages_recipients', kwargs={'message_id': f.id})
				#success_url = reverse('messages_recipients', kwargs={'meta_message_id': m.id})
			if 'next' in request.GET:
				success_url = request.GET['next']
			if 'next' in request.POST:
				success_url = request.POST['next']
			return HttpResponseRedirect(success_url)

	return render(request, 'feed.html', {'feed_message_list': feed_message_list, 'user': user, 'like_form': like_form, 'compose_form': compose_form, })

def initial_feed(request, user, *args, **kwargs):

	try:
		profile = UserProfile.objects.get(user=user)

	except UserProfile.DoesNotExist:
		UserProfile.objects.create(user=user)
	
		message_list = Message.objects.order_by('?')[:5]

		for i in range(len(message_list)):
			new_spread_message = SpreadMessage(user=user,msg=message_list[i])
			new_spread_message.save()
	# print message_list

	return

@login_required
def compose(request, form_class=ComposeForm, success_url=None):
	if request.method == "POST":
		user = request.user
		form = form_class(data=request.POST)

		recipient_list = User.objects.order_by('?')[:12]

		print recipient_list

		if form.is_valid():
			f = form.save(commit=False)
			f.creator = request.user
			f.creation_time = timezone.now()
			f.save()
			print f

			for i in range(len(recipient_list)):
				new_spread_message = SpreadMessage(user=recipient_list[i],msg=f)
				new_spread_message.save()
			messages.info(request, u"Message successfully sent.")
			if success_url is None:
				success_url = reverse('messages_recipients', kwargs={'message_id': f.id})
				#success_url = reverse('messages_recipients', kwargs={'meta_message_id': m.id})
			if 'next' in request.GET:
				success_url = request.GET['next']
			if 'next' in request.POST:
				success_url = request.POST['next']
			return HttpResponseRedirect(success_url)
	else:
		form = form_class()
	return render(request, 'compose.html', {'form': form, })

@login_required
def like(request, message_id):
	user = request.user
	profile = UserProfile.objects.get(user=user)
	message_id = request.POST.get('identifier')
	
	response_data = {}
	
	try:
		message=get_object_or_404(Message, id=message_id)
	except:
		pass
	if request.method == "POST":
		recipient_list = []
		message_like = MessageLike.objects.get_or_create(user=user, msg=message)[0]
		
		message_like.is_liked = not message_like.is_liked
		response_data['result'] = message_like.is_liked
		response_data['message'] = message.id

		if message_like.ever_liked == False:
			message_like.ever_liked = True
			message_like.save()

			# Updating promoter score

			if profile.promoter_score_last_updated is None:
				profile.promoter_score_last_updated = timezone.now()
				profile.save()

			dt = timezone.now() - profile.promoter_score_last_updated
			hours_since_update = dt.seconds / 60 / 60
			
			profile.promoter_score_update_level = profile.promoter_score_update_level - hours_since_update

			if profile.promoter_score_update_level < 4:
				profile.promoter_score_last_updated = timezone.now()
				profile.promoter_score += 5
				profile.promoter_score_update_level += 1

				profile.save()

			# Spreading

			#recipient_list = [User.objects.order_by('?')[i] for i in range(5)]

			for i in range(5):
				u = User.objects.order_by('?')[0]
				s = SpreadMessage.objects.filter(user=u,msg=message)
				if not s and message.creator != u:
					new_spread_message = SpreadMessage(user=u,msg=message)
					new_spread_message.save()
				
		else:
			message_like.save()

		# for idx,val in enumerate(recipient_list):
		# 	response_data['recipient_'+str(idx)]=val.profile.pic.url
	print response_data
	return HttpResponse(json.dumps(response_data), content_type='application/json')
#	return redirect('/')

def play(request, message_id):
	message_id = request.POST.get('identifier')
	platform = request.POST.get('platform')
	print message_id, platform

	response_data = {}

	try:
		message=get_object_or_404(Message, id=message_id)
	except:
		pass
	if request.method == "POST":
		try:
			user = request.user
			profile = UserProfile.objects.get(user=user)
			track_play = TrackPlay.objects.create(user=user, msg=message, platform=platform, played_at=timezone.now())
		except:
			track_play = TrackPlay.objects.create(msg=message, platform=platform, played_at=timezone.now())

	response_data['message'] = message.id

	return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required
def delete(request, message_id):
	user = request.user
	message = get_object_or_404(Message, id=message_id)
	deleted = False
	if request.method == "POST":
		message.delete()
		deleted = True
	if deleted == True:
		return redirect('/')
	print deleted
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required
# def delete(request, message_id, success_url=None):
# 	user = request.user
# 	now = timezone.now()
# 	message = get_object_or_404(Message, id=message_id)
# 	deleted = False
# 	if success_url is None:
# 		success_url = reverse('messages_inbox')
# 	if 'next' in request.GET:
# 		success_url = request.GET['next']
# 	if message.sender == user:
# 		message.sender_deleted_at = now
# 		deleted = True
# 	if message.recipient == user:
# 		message.recipient_deleted_at = now
# 		deleted = True
# 	if deleted:
# 		message.save()
# 		messages.info(request, u"Message successfully deleted.")
# 		return HttpResponseRedirect(success_url)
# 	raise Http404

@login_required
def undelete(request, message_id, success_url=None):
	user = request.user
	message = get_object_or_404(Message, id=message_id)
	undeleted = False
	if success_url is None:
		success_url = reverse('messages_inbox')
	if 'next' in request.GET:
		success_url = request.GET['next']
	if message.sender == user:
		message.sender_deleted_at = None
		undeleted = True
	if message.recipient == user:
		message.recipient_deleted_at = None
		undeleted = True
	if undeleted:
		message.save()
		messages.info(request, u"Message successfully recovered.")
		return HttpResponseRedirect(success_url)
	raise Http404


def messageview(request, message_id):
	message = get_object_or_404(Message, id=message_id)
	# view_count = message.message_spreadmessages.all().count() + user.profile.get_followers().count()
	prop_count = message.message_likes.filter(ever_liked=1).count()

	recipients = [m.user.profile for m in message.message_spreadmessages.all()][:6]
	proppers = [m.user.profile for m in message.message_likes.all()][:6] 

	youtube_id = None
	if re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body):
		youtube_s = re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body).group(0)
		youtube_string = "http://"+youtube_s

		url_data = urlparse.urlparse(youtube_string)
		query = urlparse.parse_qs(url_data.query)
		youtube_id = query["v"][0]
	print youtube_id

	client = soundcloud.Client(client_id='0dade5038dabd4be328a885dde4d5e0e')

	soundcloud_info = ''

	if re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body):
		soundcloud_s = re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body).group(0)
		track_url = "https://"+soundcloud_s

		print soundcloud_s
		print track_url

		embed_info = client.get('/oembed', url=track_url)

		old_soundcloud_info = embed_info.html

		print old_soundcloud_info
		old_soundcloud_info = old_soundcloud_info[:-10]
		print old_soundcloud_info

		soundcloud_info = old_soundcloud_info + " class='iframeplayer'></iframe>"

		print soundcloud_info


	try:
		user = request.user

		like_status = message.is_liked_by_user(user)
		ever_like_status = message.ever_liked_by_user(user)

	except:
		like_status = False
		ever_like_status = False
	# print like_status
	# print ever_like_status

	like_form = MessageLikeForm(initial={'is_liked': like_status, })
	return render(request, 'message.html', {'user': user, 'message': message, 'prop_count': prop_count, 'like_form': like_form, 'like_status': like_status, 'ever_like_status': ever_like_status, 'youtube_id': youtube_id, 'recipients': recipients, 'proppers': proppers, 'soundcloud_info': soundcloud_info, })

@login_required
def view(request, message_id, form_class=ComposeForm, like_form=None, subject_template=u"Re: %(subject)s"):
	user = request.user
	now = timezone.now()
	message = get_object_or_404(Message, id=message_id)
	if (message.sender != user) and (message.recipient != user):
		raise Http404
	if message.read_at is None and message.recipient == user:
		message.read_at = now
		message.save()

	context = {'message': message, 'reply_form': None}
	if message.recipient == user:
		form = form_class(initial={
			#'body': (message.sender, message.body),
			'subject': subject_template % {'subject': message.subject},
			'recipient': [message.sender,]
			})
		like_form = MessageLikeForm(initial={'is_liked': message.is_liked, })
		context['reply_form'] = form
		context['like_form'] = like_form
	return render(request, 'view.html', context, )

@login_required
def recipients(request, message_id):
	user = request.user
	message = get_object_or_404(Message, id=message_id)
	if user == message.creator:
		spread_messages = message.message_spreadmessages.all()
		return render(request, 'recipients.html', {'user': user, 'message': message, 'spread_messages': spread_messages, })
	else:
		return redirect('/')

@login_required
def follow(request, user_id):
	user = request.user
	user_id = request.POST.get('identifier')
	print user_id
	response_data = {}
	followed_user = get_object_or_404(UserProfile, id=user_id)
	if user.profile.is_following(followed_user):
		user.profile.remove_relationship(to_person=followed_user, status=1)
		response_data['result'] = 'Unfollowed'
		response_data['next_action'] = 'Follow'
	else:
		print Relationship.objects.filter(from_person=user.profile,status=1).count()
		if Relationship.objects.filter(from_person=user.profile,status=1).count() >= 100:
			print "You can only follow 100 artists at a time!"
		else:
			user.profile.add_relationship(to_person=followed_user, status=1)
		response_data['result'] = 'Followed'
		response_data['next_action'] = 'Unfollow'
	return HttpResponse(json.dumps(response_data), content_type='application/json')
#	return redirect('/')

@login_required
def stats(request, message_id):
	user = request.user
	message = get_object_or_404(Message, id=message_id)

	if user == message.creator:

		view_count = message.message_spreadmessages.all().count() + user.profile.get_followers().count()
		prop_count = message.message_likes.filter(ever_liked=1).count()
		play_count = message.message_track_plays.all().count()

		recipients = [m.user.profile for m in message.message_spreadmessages.all()][:6]
		proppers = [m.user.profile for m in message.message_likes.all()][:6] 

		youtube_id = None
		if re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body):
			youtube_s = re.search("(http\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.\S+", message.body).group(0)
			youtube_string = "http://"+youtube_s

			url_data = urlparse.urlparse(youtube_string)
			query = urlparse.parse_qs(url_data.query)
			youtube_id = query["v"][0]
		print youtube_id

		client = soundcloud.Client(client_id='0dade5038dabd4be328a885dde4d5e0e')

		soundcloud_info = ''

		if re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body):
			soundcloud_s = re.search("(www\.)?(soundcloud\.com)\/.\S+", message.body).group(0)
			track_url = "https://"+soundcloud_s

			print soundcloud_s
			print track_url

			embed_info = client.get('/oembed', url=track_url)

			soundcloud_info = embed_info.html

		return render(request, 'stats.html', {'user': user, 'message': message, 'view_count': view_count, 'prop_count': prop_count, 'play_count': play_count, 'youtube_id': youtube_id, 'recipients': recipients, 'proppers': proppers, 'soundcloud_info': soundcloud_info, })
	else:
		return redirect('/')

def all(request):
	user = request.user

	message_list = Message.objects.all().order_by('-creation_time')
	prop_count_list = []
	hotness_list = []

	for message in message_list:
		prop_count = message.message_likes.filter(ever_liked=1).count()
		prop_count_list.append(prop_count)
		naive_time = message.creation_time.replace(tzinfo=None)
		
		hotness = hot(prop_count, naive_time)
		hotness_list.append(hotness)

	param_list = [[message_list[i], prop_count_list[i], hotness_list[i]] for i in range(len(message_list))]
	parameter_list = sorted(param_list, key=itemgetter(2), reverse=True)
	print parameter_list
	
	return render(request, 'category.html', {'parameter_list': parameter_list, 'user': user, })


def trap(request):
	user = request.user

	message_list = Message.objects.filter(genre=1).order_by('-creation_time')
	prop_count_list = []
	hotness_list = []

	for message in message_list:
		prop_count = message.message_likes.filter(ever_liked=1).count()
		prop_count_list.append(prop_count)
		naive_time = message.creation_time.replace(tzinfo=None)
		
		hotness = hot(prop_count, naive_time)
		hotness_list.append(hotness)

	param_list = [[message_list[i], prop_count_list[i], hotness_list[i]] for i in range(len(message_list))]
	parameter_list = sorted(param_list, key=itemgetter(2), reverse=True)
	print parameter_list
	
	return render(request, 'category.html', {'parameter_list': parameter_list, 'user': user, })

def traptop(request):
	user = request.user

	message_list = Message.objects.filter(genre=1).order_by('-creation_time')
	prop_count_list = []

	for message in message_list:
		prop_count = message.message_likes.filter(ever_liked=1).count()
		prop_count_list.append(prop_count)

	param_list = [[message_list[i], prop_count_list[i]] for i in range(len(message_list))]
	parameter_list = sorted(param_list, key=itemgetter(1), reverse=True)

	print message_list
	return render(request, 'categorytop.html', {'parameter_list': parameter_list, 'user': user, })

def house(request):
	user = request.user

	message_list = Message.objects.filter(genre=2).order_by('-creation_time')
	prop_count_list = []
	hotness_list = []

	for message in message_list:
		prop_count = message.message_likes.filter(ever_liked=1).count()
		prop_count_list.append(prop_count)
		naive_time = message.creation_time.replace(tzinfo=None)
		
		hotness = hot(prop_count, naive_time)
		hotness_list.append(hotness)

	param_list = [[message_list[i], prop_count_list[i], hotness_list[i]] for i in range(len(message_list))]
	parameter_list = sorted(param_list, key=itemgetter(2), reverse=True)
	print parameter_list
	return render(request, 'category.html', {'parameter_list': parameter_list, 'user': user, })

def trance(request):
	user = request.user

	message_list = Message.objects.filter(genre=3).order_by('-creation_time')
	prop_count_list = []
	hotness_list = []

	for message in message_list:
		prop_count = message.message_likes.filter(ever_liked=1).count()
		prop_count_list.append(prop_count)
		naive_time = message.creation_time.replace(tzinfo=None)
		
		hotness = hot(prop_count, naive_time)
		hotness_list.append(hotness)

	param_list = [[message_list[i], prop_count_list[i], hotness_list[i]] for i in range(len(message_list))]
	parameter_list = sorted(param_list, key=itemgetter(2), reverse=True)
	print parameter_list
	return render(request, 'category.html', {'parameter_list': parameter_list, 'user': user, })

def bass(request):
	user = request.user

	message_list = Message.objects.filter(genre=4).order_by('-creation_time')
	prop_count_list = []
	hotness_list = []

	for message in message_list:
		prop_count = message.message_likes.filter(ever_liked=1).count()
		prop_count_list.append(prop_count)
		naive_time = message.creation_time.replace(tzinfo=None)
		
		hotness = hot(prop_count, naive_time)
		hotness_list.append(hotness)

	param_list = [[message_list[i], prop_count_list[i], hotness_list[i]] for i in range(len(message_list))]
	parameter_list = sorted(param_list, key=itemgetter(2), reverse=True)
	print parameter_list
	return render(request, 'category.html', {'parameter_list': parameter_list, 'user': user, })

def harddance(request):
	user = request.user

	message_list = Message.objects.filter(genre=5).order_by('-creation_time')
	prop_count_list = []
	hotness_list = []

	for message in message_list:
		prop_count = message.message_likes.filter(ever_liked=1).count()
		prop_count_list.append(prop_count)
		naive_time = message.creation_time.replace(tzinfo=None)
		
		hotness = hot(prop_count, naive_time)
		hotness_list.append(hotness)

	param_list = [[message_list[i], prop_count_list[i], hotness_list[i]] for i in range(len(message_list))]
	parameter_list = sorted(param_list, key=itemgetter(2), reverse=True)
	print parameter_list
	return render(request, 'category.html', {'parameter_list': parameter_list, 'user': user, })

def fuckgenres(request):
	user = request.user

	message_list = Message.objects.filter(genre=6).order_by('-creation_time')
	prop_count_list = []
	hotness_list = []

	for message in message_list:
		prop_count = message.message_likes.filter(ever_liked=1).count()
		prop_count_list.append(prop_count)
		naive_time = message.creation_time.replace(tzinfo=None)
		
		hotness = hot(prop_count, naive_time)
		hotness_list.append(hotness)

	param_list = [[message_list[i], prop_count_list[i], hotness_list[i]] for i in range(len(message_list))]
	parameter_list = sorted(param_list, key=itemgetter(2), reverse=True)
	print parameter_list
	return render(request, 'category.html', {'parameter_list': parameter_list, 'user': user, })

def featured(request, entry_id):
	try:
		user = request.user
	except:
		pass
	entry = get_object_or_404(FeaturedEntry, id=entry_id)
	return render(request, 'featured.html', {'entry': entry, })

@staff_member_required
def featuredcompose(request,entry_form=FeaturedEntryForm):
	if request.method == "POST":
		form = entry_form(request.POST, request.FILES)
		if form.is_valid():
			f = form.save()
			print f
			return redirect('/')
	else:
		form = entry_form()
	return render(request, 'featuredcompose.html', {'form': form, })
	
@staff_member_required
def featurededit(request, entry_id):
	entry = get_object_or_404(FeaturedEntry, id=entry_id)
	form = FeaturedEntryForm(initial={'artist_name': entry.artist_name, 'entry_text': entry.entry_text, 'artist_image': entry.artist_image, 'song_link1': entry.song_link1, 'song_link2': entry.song_link2, 'song_link3': entry.song_link3, })
	return render(request, 'featurededit.html', {'entry': entry, 'form': form, })

@staff_member_required
def update_featuredentry(request, entry_id):
	try:
		entry=FeaturedEntry.objects.get(id=entry_id)
	except:
		pass
	if request.method=='POST':
		form = FeaturedEntryForm(request.POST, request.FILES, instance=entry)
		if form.is_valid():
			form.save()
	return redirect('/')