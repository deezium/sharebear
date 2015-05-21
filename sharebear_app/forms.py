from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django import forms
from sharebear_app.models import UserProfile, SpreadMessage, MessageLike, FeaturedEntry
from django.conf import settings
from django.utils import timezone
from sharebear_app.models import Message
from sharebear_app.fields import CommaSeparatedUserField

class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
	last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
	password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

	class Meta:
		fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
		model = User

class UsernameEditForm(forms.ModelForm):
	username=forms.CharField(required=False, label='Username', widget=forms.widgets.TextInput())
	
	class Meta:
		fields =['username']
		model = User

class EditProfileForm(forms.ModelForm):
	pic = forms.ImageField(required=False)
	aboutme = forms.CharField(required=False, label='About me', widget=forms.Textarea(attrs={'placeholder': 'You are awesome.'}))
	location = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'Where you at?'}))
	soundcloud_page = forms.CharField(required=False, label='', widget=forms.widgets.TextInput(attrs={'placeholder': 'Soundcloud Page'}))
	facebook_page = forms.CharField(required=False, label='', widget=forms.widgets.TextInput(attrs={'placeholder': 'Facebook Page'}))

	class Meta:
		fields = ['pic', 'location', 'aboutme', 'soundcloud_page', 'facebook_page']
		model = UserProfile

class AuthenticateForm(AuthenticationForm):
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
	

class ComposeForm(forms.ModelForm):
	body = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Post your latest hotness.'}))
	
	class Meta:
		fields = ['body', 'genre']
		model = Message

class FeaturedEntryForm(forms.ModelForm):
	artist_name = forms.CharField(widget=forms.widgets.TextInput())
	entry_text = forms.CharField(widget=forms.Textarea())
	artist_image = forms.ImageField(required=False)
	profile_link = forms.widgets.TextInput()
	song_link1 = forms.CharField(widget=forms.Textarea())
	song_link2 = forms.CharField(widget=forms.Textarea())
	song_link3 = forms.CharField(widget=forms.Textarea())

	class Meta:
		fields = ['artist_name', 'entry_text', 'artist_image', 'profile_link', 'song_link1', 'song_link2', 'song_link3']
		model = FeaturedEntry

class MessageLikeForm(forms.ModelForm):
	is_liked = forms.BooleanField(widget=forms.widgets.CheckboxInput())

	class Meta:
		fields=['is_liked']
		model = MessageLike

	# def save(self, sender, recipients, meta_msg, conversation, parent_msg=None):
	# 	#recipients = self.cleaned_data['recipient']
	# 	subject = self.cleaned_data['subject']
	# 	body = self.cleaned_data['body']
	# 	#meta_sub = self.cleaned_data['meta_sub']
	# 	if parent_msg is None:
	# 		meta_message = MetaMessage()
	# 		meta_message.save()
	# 	message_list = []

	# 	for r in recipients:
	# 		if parent_msg is None:
	# 			msg = Message(sender=sender, recipient=r, subject=subject, body=body, meta_msg=meta_message)
	# 		else:
	# 			msg = Message(sender=sender, recipient=r, subject=subject, body=body, conversation=conversation, meta_msg=None)
	# 			msg.parent_msg = parent_msg
	# 			parent_msg.replied_at = timezone.now()
	# 			parent_msg.save()
	# 		msg.save()
	# 		message_list.append(msg)
	# 	return message_list

