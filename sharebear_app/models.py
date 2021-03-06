from django.db import models
from django.contrib.auth.models import User
import hashlib
from django.conf import settings
from datetime import datetime
from django.utils import timezone
#from django.utils.encoding import python_2_unicode_compatible
from allauth.socialaccount.models import SocialAccount
from social.apps.django_app.default.models import UserSocialAuth
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
	(RELATIONSHIP_FOLLOWING, 'Following'),
	(RELATIONSHIP_BLOCKED, 'Blocked')
)

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	pic = models.FileField(upload_to='avatars', default='avatars/user_icon.jpg')
	aboutme = models.TextField(null=True, blank=True, default='I am a trapaholic.')
	location = models.TextField(null=True, blank=True, default='The greatest place on Earth.')
	promoter_score = models.IntegerField(default=0)
	promoter_score_last_updated = models.DateTimeField(null=True, blank=True)
	promoter_score_update_level = models.IntegerField(default=0)
	relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')
	soundcloud_page = models.CharField(max_length=200, null=True, blank=True, default='')
	facebook_page = models.CharField(max_length=200, null=True, blank=True, default='')


	def __unicode__(self):
		return self.user.username

	def profile_image_url(self):
		fb_uid = UserSocialAuth.objects.filter(user_id=self.user.id, provider='facebook')

		if len(fb_uid) and self.pic == 'avatars/user_icon.jpg':
			print fb_uid[0].uid
			return "http://graph.facebook.com/{}/picture?width=400&height=400".format(fb_uid[0].uid)

		return self.pic.url

	def facebook_location(self):
		fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

		if len(fb_uid):
#			return "http://graph.facebook.com/{}/picture?width=100&height=100".format(fb_uid[0].uid)

			return "http://graph.facebook.com/10100397741993658/picture?width=100&height=100"

		return "No location specified"

	def add_relationship(self, to_person, status):
		relationship, created = Relationship.objects.get_or_create(
			from_person=self,
			to_person=to_person,
			status=status)
		return relationship

	def remove_relationship(self, to_person, status):
		Relationship.objects.filter(
			from_person=self,
			to_person=to_person,
			status=status).delete()
		return

	def is_following(self, user):
		if self.relationships.filter(
			to_people__status=RELATIONSHIP_FOLLOWING,
			to_people__to_person=user):
			return True
		return False

	def get_relationships(self, status):
		return self.relationships.filter(
			to_people__status=status,
			to_people__from_person=self)

	def get_related_to(self, status):
		return self.related_to.filter(
			from_people__status=status,
			from_people__to_person=self)

	def get_following(self):
		return self.get_relationships(RELATIONSHIP_FOLLOWING)

	def get_followers(self):
		return self.get_related_to(RELATIONSHIP_FOLLOWING)

	def get_reach(self):
		followers = self.get_followers().count()
		messages = self.user.sent_messages.all()
		spread_count_list = [i.message_spreadmessages.all().count() for i in messages]
		spread_view_count = sum(spread_count_list)
		follower_view_count = followers*messages.count()
		view_count = spread_view_count + follower_view_count
		return view_count

	def get_plays(self):
		messages = self.user.sent_messages.all()
		play_count_list = [m.message_track_plays.all().count() for m in messages]
		play_count = sum(play_count_list)
		return play_count

	def get_likes(self):
		messages = self.user.sent_messages.all()
		prop_count_list = [m.message_likes.filter(ever_liked=1).count() for m in messages]
		prop_count = sum(prop_count_list)
		return prop_count

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
	TRAP = 1
	HOUSE = 2
	TRANCE = 3
	BASS = 4
	HARD_DANCE = 5
	FUCK_GENRES = 6

	GENRE_CHOICES = (
		(TRAP, 'Trap'),
		(HOUSE, 'House'),
		(TRANCE, 'Trance'),
		(BASS, 'Bass'),
		(HARD_DANCE, 'Hard Dance'),
		(FUCK_GENRES, 'Fuck Genres'),
		)

	body = models.TextField("Body")
	creator = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_messages', verbose_name="Sender")
	creation_time = models.DateTimeField("Sent at", null=True, blank=True)
	genre = models.IntegerField(max_length=40, choices=GENRE_CHOICES, default=FUCK_GENRES, blank=False)

	# objects = MessageManager()

	def __unicode__(self):
		return self.body

	def get_absolute_url(self):
		return reverse('messages_detail', args=[str(self.id)])

	def save(self, **kwargs):
		if not self.id:
			self.creation_time = timezone.now()
		super(Message, self).save(**kwargs)

	def is_liked_by_user(self, user):
		like = self.message_likes.filter(user=user)
		for i in like:
			return i.is_liked
		return False

	def ever_liked_by_user(self, user):
		like = self.message_likes.filter(user=user)
		for i in like:
			return i.ever_liked
		return False

	class Meta:
		ordering = ['-creation_time']
		verbose_name = "Message"
		verbose_name_plural = "Messages"

class MessageLike(models.Model):
	user = models.ForeignKey(AUTH_USER_MODEL, related_name='user_likes', verbose_name="Liking user")
	msg = models.ForeignKey(Message, related_name='message_likes')
	is_liked = models.BooleanField("Liked", default=False)
	ever_liked = models.BooleanField("Ever Liked", default=False)
	liked_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.id)

class FeaturedEntry(models.Model):
	artist_name = models.CharField(max_length=40)
	entry_text = models.TextField()
	artist_image = models.FileField(upload_to='avatars', default='avatars/user_icon.jpg')
	profile_link = models.CharField(max_length=200, null=True, blank=True)
	song_link1 = models.TextField()
	song_link2 = models.TextField(null=True, blank=True)
	song_link3 = models.TextField(null=True, blank=True)
	post_time = models.DateTimeField("Posted at", auto_now=True, null=True, blank=True)
	current_followers = models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.id)

	def get_next(self):
		next_entry = FeaturedEntry.objects.filter(id__gt=self.id)
		if next_entry:
			return next_entry[0]
		return False

	def get_prev(self):
		prev_entry = FeaturedEntry.objects.filter(id__lt=self.id).order_by('-id')
		print prev_entry
		if prev_entry:
			return prev_entry[0]
		return False


class SocialShare(models.Model):
	user = models.ForeignKey(AUTH_USER_MODEL, related_name='user_social_shares', verbose_name="Sharing user")
	msg = models.ForeignKey(Message, related_name='message_social_shares')
	platform = models.CharField(max_length=40)

	def __unicode__(self):
		return str(self.id)

class TrackPlay(models.Model):
	user = models.ForeignKey(AUTH_USER_MODEL, related_name='user_track_plays', blank=True, null=True)
	msg = models.ForeignKey(Message, related_name='message_track_plays')
	platform = models.CharField(max_length=40)
	played_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.id)

class Relationship(models.Model):
	from_person = models.ForeignKey(UserProfile, related_name='from_people')
	to_person = models.ForeignKey(UserProfile, related_name='to_people')
	status = models.IntegerField(choices=RELATIONSHIP_STATUSES)

	class Meta:
		unique_together = (("from_person", "to_person", "status"),)

class SpreadMessage(models.Model):
	user = models.ForeignKey(AUTH_USER_MODEL, related_name='user_spreadmessages')
	msg = models.ForeignKey(Message, related_name='message_spreadmessages')

	#class Meta:
	#	unique_together = (("user", "msg"),)

	def __unicode__(self):
		return str(self.id)

class CampaignRequest(models.Model):
	name = models.CharField(max_length=40)
	email = models.CharField(max_length=60)
	url = models.CharField(max_length=200)
	details = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.url