from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django import forms
from sharebear_app.models import UserProfile
from django.conf import settings
from django.utils import timezone
from sharebear_app.models import Message, MetaMessage
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

class EditProfileForm(forms.ModelForm):
	pic = forms.ImageField(required=False)
	aboutme = forms.CharField(required=False, label='About me', widget=forms.Textarea(attrs={'placeholder': 'What is awesome about you?'}))
	location = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'Where you at?'}))

	class Meta:
		fields = ['pic', 'location', 'aboutme']
		model = UserProfile

class AuthenticateForm(AuthenticationForm):
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
	

class MessageLikeForm(forms.ModelForm):
	is_liked = forms.BooleanField(widget=forms.widgets.CheckboxInput())

	class Meta:
		fields = ['is_liked']
		model = Message

class ComposeForm(forms.Form):
	#recipient = CommaSeparatedUserField(label="Recipients", widget=forms.widgets.TextInput(attrs={'placeholder': 'Enter usernames here'}))
	subject = forms.CharField(label="Subject", max_length=140, widget=forms.widgets.TextInput(attrs={'placeholder': 'Enter subject here'}))
	body = forms.CharField(label="Body", widget=forms.Textarea(attrs={'placeholder': 'Enter your message here'}))
	#meta_sub = forms.CharField(label="Meta Subject", max_length=140, widget=forms.widgets.TextInput(attrs={'placeholder': 'Meta Subject'}))

	def __init__(self, *args, **kwargs):
		recipient_filter = kwargs.pop('recipient_filter', None)
		super(ComposeForm, self).__init__(*args, **kwargs)
		if recipient_filter is not None:
			self.fields['recipient']._recipient_filter = recipient_filter

	def save(self, sender, recipients, meta_msg, conversation, parent_msg=None):
		#recipients = self.cleaned_data['recipient']
		subject = self.cleaned_data['subject']
		body = self.cleaned_data['body']
		#meta_sub = self.cleaned_data['meta_sub']
		if parent_msg is None:
			meta_message = MetaMessage()
			meta_message.save()
		message_list = []

		for r in recipients:
			if parent_msg is None:
				msg = Message(sender=sender, recipient=r, subject=subject, body=body, meta_msg=meta_message)
			else:
				msg = Message(sender=sender, recipient=r, subject=subject, body=body, conversation=conversation, meta_msg=None)
				msg.parent_msg = parent_msg
				parent_msg.replied_at = timezone.now()
				parent_msg.save()
			msg.save()
			message_list.append(msg)
		return message_list


	# def save(self, sender, commit=True):
	# 	form = super(ComposeForm, self).save(commit=False)
	# 	recipients = self.cleaned_data['recipient']
	# 	meta_sub = self.cleaned_data['meta_sub']
	# 	meta_message = MetaMessage(meta_sub=meta_sub, )
	# 	meta_message.save()
	# 	message_list = []

	# 	for r in recipients:
	# 		msg = Message(sender=sender, recipient=r, subject=subject, body=body, meta_msg=meta_message)
	# 		if parent_msg is not None:
	# 			msg.parent_msg = parent_msg
	# 			parent_msg.replied_at = timezone.now()
	# 			parent_msg.save()
	# 		msg.save()
	# 		message_list.append(msg)
	# 	if commit:
	# 		form.save()
	# 	return form

	# class Meta:
	# 	fields = ['recipient', 'subject', 'body', 'meta_sub']
	# 	model = Message

