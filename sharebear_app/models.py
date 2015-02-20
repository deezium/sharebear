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
	promoter_score = models.IntegerField(default=0)
	promoter_score_last_updated = models.DateTimeField(null=True, blank=True)
	promoter_score_update_level = models.IntegerField(default=0)

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


# class MetaMessage(models.Model):

# 	objects = MetaMessageManager()

# 	def __unicode__(self):
# 		return str(self.id)

# 	def get_absolute_url(self):
# 		return reverse('meta_messages_detail', args=[str(self.id)])


# class MessageManager(models.Manager):

# 	def inbox_for(self, user):
# 		return self.filter(recipient=user, recipient_deleted_at__isnull=True, )

# 	def outbox_for(self, user):
# 		return self.filter(sender=user, sender_deleted_at__isnull=True, )

# 	def convo_outbox_for(self, user):
# 		return self.filter(sender=user, sender_deleted_at__isnull=True, parent_msg__isnull=False, )

# 	def trash_for(self, user):
# 		return self.filter(recipient=user, recipient_deleted_at__isnull=False, ) | self.filter(sender=user, sender_deleted_at__isnull=False, )

# 	def feed_for(self, user):
# 		return self.filter(recipient=user)


class Message(models.Model):
	body = models.TextField("Body")
	creator = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_messages', verbose_name="Sender")
	creation_time = models.DateTimeField("Sent at", null=True, blank=True)

	# objects = MessageManager()

	def __unicode__(self):
		return self.body

	def get_absolute_url(self):
		return reverse('messages_detail', args=[str(self.id)])

	def save(self, **kwargs):
		if not self.id:
			self.creation_time = timezone.now()
		super(Message, self).save(**kwargs)

	class Meta:
		ordering = ['-creation_time']
		verbose_name = "Message"
		verbose_name_plural = "Messages"

class FeedStory(models.Model):
	user = models.ForeignKey(AUTH_USER_MODEL, related_name='feed_stories', verbose_name="Recipient")
	msg = models.ForeignKey(Message, related_name='feed_messages')
	is_liked = models.BooleanField("Liked", default=False)
	ever_liked = models.BooleanField("Ever Liked", default=False)

	def __unicode__(self):
		return str(self.id)
