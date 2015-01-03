from django.db import models
from django.contrib.auth.models import User
import hashlib
from django.conf import settings
from datetime import datetime
from django.utils import timezone
#from django.utils.encoding import python_2_unicode_compatible
from allauth.socialaccount.models import SocialAccount
from django.core.urlresolvers import reverse

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	pic = models.FileField(upload_to='avatars', default='avatars/finger.jpg')
	aboutme = models.TextField(null=True, blank=True)
	location = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.user.username

	def profile_image_url(self):
		fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

		if len(fb_uid):
			print fb_uid[0].uid
			return "http://graph.facebook.com/{}/picture?width=100&height=100".format(fb_uid[0].uid)

		return self.pic.url

	def facebook_location(self):
		fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

		if len(fb_uid):
#			return "http://graph.facebook.com/{}/picture?width=100&height=100".format(fb_uid[0].uid)

			return "http://graph.facebook.com/10100397741993658/picture?width=100&height=100"

		return "No location specified"


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class MetaMessageManager(models.Manager):

	# def metaoutbox_for(self, user):
	# 	s = self.model
	# 	return self.filter(s=user, )

	pass

class MetaMessage(models.Model):
	#meta_sub = models.CharField("Meta Subject", max_length=140)

	objects = MetaMessageManager()

	def __unicode__(self):
		return str(self.id)

	def get_absolute_url(self):
		return reverse('meta_messages_detail', args=[str(self.id)])

class Conversation(models.Model):

	def __unicode__(self):
		return str(self.id)


class MessageManager(models.Manager):

	def inbox_for(self, user):
		return self.filter(recipient=user, recipient_deleted_at__isnull=True, )

	def outbox_for(self, user):
		return self.filter(sender=user, sender_deleted_at__isnull=True, )

	def convo_outbox_for(self, user):
		return self.filter(sender=user, sender_deleted_at__isnull=True, parent_msg__isnull=False, )

	def trash_for(self, user):
		return self.filter(recipient=user, recipient_deleted_at__isnull=False, ) | self.filter(sender=user, sender_deleted_at__isnull=False, )

	def feed_for(self, user):
		return self.filter(recipient=user)


class Message(models.Model):
	subject = models.CharField("Subject", max_length=140)
	body = models.TextField("Body")
	sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_messages', verbose_name="Sender")
	recipient = models.ForeignKey(AUTH_USER_MODEL, related_name='received_messages', verbose_name="Recipients")
	parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True, verbose_name="Parent Message")
	meta_msg = models.ForeignKey(MetaMessage, related_name='sub_messages', blank=True, null=True)
	conversation = models.ForeignKey(Conversation, related_name='convo_messages', verbose_name="Conversation", blank=True, null=True)
	sent_at = models.DateTimeField("Sent at", null=True, blank=True)
	read_at = models.DateTimeField("Read at", null=True, blank=True)
	replied_at = models.DateTimeField("Replied at", null=True, blank=True)
	sender_deleted_at = models.DateTimeField("Sender deleted at", null=True, blank=True)
	recipient_deleted_at = models.DateTimeField("Recipient deleted at", null=True, blank=True)
	is_liked = models.BooleanField("Liked", default=False)

	objects = MessageManager()

	def __unicode__(self):
		return self.subject

	def new(self):
		if self.read_at is not None:
			return False
		return True

	def replied(self):
		if self.replied_at is not None:
			return False
		return True

	def get_absolute_url(self):
		return reverse('messages_detail', args=[str(self.id)])

	def save(self, **kwargs):
		if not self.id:
			self.sent_at = timezone.now()
		super(Message, self).save(**kwargs)

	class Meta:
		ordering = ['-sent_at']
		verbose_name = "Message"
		verbose_name_plural = "Messages"

def inbox_count_for(user):
	return Message.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True)

