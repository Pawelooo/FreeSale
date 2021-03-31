from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from django import forms
from users.models import UserInfo, Message, Conversation


class UserCreateEmailForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        field_classes = {'username': UsernameField}


class UserInfoUpdateForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['phone', 'image']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ConversationCreateForm(Form):
    message = forms.CharField(widget=forms.Textarea)


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']


class ConversationForm(ModelForm):
    class Meta:
        model = Conversation
        fields = '__all__'


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []
