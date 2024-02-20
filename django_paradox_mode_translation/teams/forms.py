from django import forms

from teams.models import TeamInvites


class InviteUserForm(forms.ModelForm):

    text_invite = forms.CharField(
        max_length=500,
        label='Приглашение',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 10,
            'col': 50
        })
    )

    class Meta:
        model = TeamInvites
        fields = ['text_invite']
