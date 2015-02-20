from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from collections import OrderedDict
from sharebear_app.forms import AuthenticateForm, UserCreateForm, EditProfileForm, ComposeForm, FeedStoryLikeForm
from sharebear_app.models import UserProfile, Message, FeedStory
from sharebear_app.utils import get_user_model, get_username_field
from urllib2 import urlopen
import json

User = get_user_model()

def index(request, auth_form=None, user_form=None):
	if request.user.is_authenticated():
		user = request.user
		return redirect('/feed/')
	else:
		auth_form = auth_form or AuthenticateForm()
		user_form = user_form or UserCreateForm()
		return render(request, 'home.html', {'auth_form': auth_form, 'user_form': user_form, })

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

def get_latest(user):
	try:
		return user.visit_set.order_by('-id')[0]
	except IndexError:
		return ""

def users(request, username="", edit_form=None):
	user = request.user
	if username:
		try:
			profile_user = User.objects.get(username=username)
			userprofile = UserProfile.objects.get_or_create(user=profile_user)
		except User.DoesNotExist:
			raise Http404
		if profile_user == request.user:
			edit_form = EditProfileForm(initial={'location': user.profile.location, 'aboutme':user.profile.aboutme, })
		print profile_user.feed_stories.all()
		# if username == request.user.username:
		# 	return redirect('/')
		# 	return render(request, 'profile.html', {'user': user, 'visits': visits, 'visit_form': visit_form, })
		return render(request, 'profile.html', {'next_url': '/users/%s' % user.username, 'profile_user': profile_user, 'user': user, 'userprofile': userprofile, 'edit_form': edit_form, })
	users = User.objects.all()
	return redirect('/')
	#return render(request, 'users.html', {'users': users, 'username': request.user.username, })

# @login_required
# def inbox(request):
# 	user = request.user
# 	message_list = Message.objects.inbox_for(request.user)
# 	return render(request, 'inbox.html', {'message_list': message_list, 'user': user, })

# @login_required
# def conversationbox(request):
# 	user = request.user
# 	conversation_set = set()
# 	for m in Message.objects.select_related('conversation').filter(sender=request.user):
# 		conversation_set.add(m.conversation)
# 	for m in Message.objects.select_related('conversation').filter(recipient=request.user):
# 		conversation_set.add(m.conversation)
# 	print conversation_set
# 	conversation_set.remove(None)
# 	print conversation_set
# 	conversation_list = []
# 	for c in conversation_set:
# 		message = c.convo_messages.first().body
# 		other_person = c.convo_messages.first().sender if c.convo_messages.first().sender != request.user else c.convo_messages.first().recipient  
# 		latest_sender = c.convo_messages.first().sender
# 		timestamp = c.convo_messages.first().sent_at
# 		conversation_list.append([message,other_person,latest_sender,timestamp,c])
# 	return render(request, 'conversationbox.html', {'conversation_list': conversation_list, })

@login_required
def feed(request, like_form=None):
	user = request.user
	#message_list = Message.objects.feed_for(request.user)
	feed_story_list = FeedStory.objects.filter(user=request.user)
	like_form=FeedStoryLikeForm()
	return render(request, 'feed.html', {'feed_story_list': feed_story_list, 'user': user, 'like_form': like_form, })

# @login_required
# def outbox(request):
# 	user = request.user
# 	message_list = Message.objects.convo_outbox_for(request.user)
# 	return render(request, 'outbox.html', {'message_list': message_list, })

# @login_required
# def trash(request):
# 	user = request.user
# 	message_list = Message.objects.trash_for(request.user)
# 	return render(request, 'trash.html', {'message_list': message_list, })

@login_required
def compose(request, form_class=ComposeForm, success_url=None):
	if request.method == "POST":
		user = request.user
		form = form_class(data=request.POST)

		recipient_list = [User.objects.order_by('?')[i] for i in range(5)]

		if form.is_valid():
			f = form.save(commit=False)
			f.creator = request.user
			f.creation_time = timezone.now()
			f.save()
			print f

			for i in range(5):
				new_feed_story = FeedStory(user=recipient_list[i],msg=f)
				new_feed_story.save()
			messages.info(request, u"Message successfully sent.")
			if success_url is None:
				success_url = reverse('messages_compose')
				#success_url = reverse('messages_recipients', kwargs={'meta_message_id': m.id})
			if 'next' in request.GET:
				success_url = request.GET['next']
			if 'next' in request.POST:
				success_url = request.POST['next']
			return HttpResponseRedirect(success_url)
	else:
		form = form_class()
	return render(request, 'compose.html', {'form': form, })

# @login_required
# def reply(request, message_id, form_class=ComposeForm, success_url=None, recipient_filter=None, subject_template=u"Re: %(subject)s"):
# 	parent = get_object_or_404(Message, id=message_id)
# 	if parent.sender != request.user and parent.recipient != request.user:
# 		raise Http404

# 	# Note that replying doesn't create a meta message

# 	if request.method == "POST":
# 		sender = request.user
# 		form = form_class(request.POST, recipient_filter=recipient_filter)

# 		if form.is_valid():
# 			f = form.save(sender=request.user, recipients=[parent.sender], parent_msg=parent)
# 			messages.info(request, u"Message successfully sent.")
# 			print f

# 			# m = MetaMessage.objects.get(id=parent.meta_msg.id)
# 			# message = m.sub_messages.first()
# 			# for i in range(10):
# 			# 	new_message=Message(subject=message.subject,
# 			# 		body=message.body,
# 			# 		sender=message.sender,
# 			# 		recipient=User.objects.order_by('?')[0],
# 			# 		meta_msg=m,
# 			# 		sent_at=datetime.now()
# 			# 		)
# 			# 	new_message.save()

# 			if success_url is None:
# 				success_url = reverse('messages_inbox')
# 			return HttpResponseRedirect(success_url)
# 	else:
# 		form = form_class(initial={
# 			#'body': (parent.sender, parent.body),
# 			'subject': subject_template % {'subject': parent.subject},
# 			'recipient': [[parent.sender,]]
# 			})
# 	return render(request, 'compose.html', {'form': form, })

# @login_required
# def feedreply(request, user_id,form_class=ComposeForm, subject_template=u"Re: %(subject)s"):
# 	user = request.user
# 	other_user = User.objects.get(id=user_id)
# 	print user, other_user

# 	conversation = get_object_or_404(Conversation, id=3)
# 	messages = conversation.convo_messages.all().order_by('sent_at')

# 	reply_form = form_class(initial={
# 		'subject': subject_template % {'subject': messages.last().subject},
# 		})
# 	return render(request, 'conversation.html', {'conversation': conversation, 'messages': messages, 'reply_form': reply_form, })

@login_required
def like(request, feed_story_id):
	user = request.user
	profile = UserProfile.objects.get(user=user)
	try:
		feed_story=get_object_or_404(FeedStory, id=feed_story_id)
	except:
		pass
	if request.method == "POST":
		
		feed_story.is_liked = not feed_story.is_liked
		if feed_story.ever_liked == False:
			feed_story.ever_liked = True
			feed_story.save()

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

			# Creating more feed stories

			m = Message.objects.get(id=feed_story.msg.id)

			recipient_list = [User.objects.order_by('?')[i] for i in range(4)]

			for i in range(4):
				new_feed_story=FeedStory(user=recipient_list[i],
					msg=m,
					is_liked=False,
					ever_liked=False,
					)
				new_feed_story.save()
				print new_feed_story
			
		else:
			feed_story.save()
		
	return redirect('/')

@login_required
def delete(request, message_id, success_url=None):
	user = request.user
	now = timezone.now()
	message = get_object_or_404(Message, id=message_id)
	deleted = False
	if success_url is None:
		success_url = reverse('messages_inbox')
	if 'next' in request.GET:
		success_url = request.GET['next']
	if message.sender == user:
		message.sender_deleted_at = now
		deleted = True
	if message.recipient == user:
		message.recipient_deleted_at = now
		deleted = True
	if deleted:
		message.save()
		messages.info(request, u"Message successfully deleted.")
		return HttpResponseRedirect(success_url)
	raise Http404

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

@login_required
def messageview(request, message_id):
	user = request.user
	message = get_object_or_404(Message, id=message_id)
	view_count = message.feed_messages.count()
	prop_count = message.feed_messages.filter(ever_liked=1).count()
	
	return render(request, 'message.html', {'user': user, 'message': message, 'view_count': view_count, 'prop_count': prop_count, })

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
	return render(request, 'recipients.html', {'user': user, 'message': message, })

# @login_required
# def metaoutbox(request):
# 	user = request.user
# 	m = Message.objects.filter(sender=user).order_by('-sent_at')
# 	messages = [message.meta_msg for message in m]
# 	message_list = list(OrderedDict.fromkeys(messages))

# 	return render(request, 'metaoutbox.html', {'message_list': message_list, })

# @login_required
# def metaview(request, meta_message_id):
# 	user = request.user
# 	meta_message = get_object_or_404(MetaMessage, id=meta_message_id)
# 	# print user
# 	# Prevent viewing of message unless you're the sender
# 	# if (message.sender != user) and (message.recipient != user):
	
# 	# raise Http404

# 	return render(request, 'metaview.html', {'meta_message': meta_message, })

# @login_required
# def conversations(request, conversation_id, form_class=ComposeForm, subject_template=u"Re: %(subject)s"):
# 	user = request.user
# 	conversation = get_object_or_404(Conversation, id=conversation_id)
# 	messages = conversation.convo_messages.all().order_by('sent_at')

# 	reply_form = form_class(initial={
# 		'subject': subject_template % {'subject': messages.last().subject},
# 		})
# 	return render(request, 'conversation.html', {'conversation': conversation, 'messages': messages, 'reply_form': reply_form, })

# @login_required
# def random(request, form_class=ComposeForm, subject_template=u"Re: %(subject)s"):
# 	user = request.user
# 	now = timezone.now()

# 	meta_message = MetaMessage.objects.order_by('?')[0]
	
# 	form = form_class(initial={
# 		'subject': subject_template % {'subject': meta_message.sub_messages.first()},
# 		'recipient': [meta_message.sub_messages.first().sender, ]
# 		})
# 	return render(request, 'random.html', {'meta_message': meta_message, 'reply_form': form, })

# @login_required
# def randomreply(request, meta_message_id, form_class=ComposeForm, success_url=None, recipient_filter=None, subject_template=u"Re: %(subject)s"):
# 	meta_msg = get_object_or_404(MetaMessage, id=meta_message_id)
	
# 	if request.method == "POST":
# 		sender = request.user
# 		form = form_class(request.POST, recipient_filter=recipient_filter)

# 		if form.is_valid():
# 			msg = meta_msg.sub_messages.first()
# 			parent = Message.objects.create(sender=msg.sender, recipient=request.user, subject=msg.subject, body=msg.body, sent_at=timezone.now(), replied_at=timezone.now())
# 			f = form.save(sender=request.user, recipients=[parent.sender], parent_msg=parent)
# 			messages.info(request, u"Message successfully sent.")
# 			if success_url is None:
# 				success_url = reverse('messages_inbox')
# 			return HttpResponseRedirect(success_url)

# 	return render(request, 'random.html', {'reply_form': form, })

# @login_required
# def convoreply(request, conversation_id, form_class=ComposeForm, success_url=None):
# 	conversation = get_object_or_404(Conversation, id=conversation_id)
	
# 	first_message = conversation.convo_messages.first()
# 	if first_message.sender == request.user:
# 		recipient = first_message.recipient
# 	else:
# 		recipient = first_message.sender
	
# 	if request.method == "POST":
# 		sender = request.user
# 		form = form_class(request.POST)
# 		parent = conversation.convo_messages.last()

# 		if form.is_valid():
# 			f = form.save(sender=sender, recipients=[recipient, ], parent_msg=parent, meta_msg=None, conversation=conversation)
# 			messages.info(request, u"Message successfully sent.")
# 			if success_url is None:
# 				success_url = reverse('conversations_detail', args=[conversation.id])
# 			print success_url
# 			return HttpResponseRedirect(success_url)
# 	return redirect('/')