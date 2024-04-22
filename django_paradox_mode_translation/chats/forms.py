from django import forms
from django.utils import timezone

from chats.models import PrivateMessage, TeamMessage


class SendMessageForm(forms.ModelForm):

    body = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': "Введите сообщение здесь",
            'type': "text",
            'class': "form-control",
        }),
        required=True,
        label="Сообщение"
    )

    def save(self, author=None, chat=None, commit=True):
        instance = super(SendMessageForm, self).save(commit=False)
        instance.author = author
        instance.chat = chat
        instance.pub_date = timezone.now()
        instance.save()
        return instance

    class Meta:
        fields = ['body']


class PrivateMessageForm(SendMessageForm):

    class Meta(SendMessageForm.Meta):
        model = PrivateMessage


class TeamMessageForm(SendMessageForm):

    class Meta(SendMessageForm.Meta):
        model = TeamMessage
