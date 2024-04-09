from django import forms

from teams.models import TeamInvites, Teams, TeamMembers


class CreateTeamForm(forms.ModelForm):

    team_title = forms.CharField(
        widget=forms.TextInput(attrs={

        }),
        label="Название команды",
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={

        }),
        required=False,
        label="Описание"
    )

    def save(self, user=None, commit=True):
        instance = super(CreateTeamForm, self).save(commit)
        if user:
            team_member, created = TeamMembers.objects.get_or_create(team=instance, user=user)
            if created:
                team_member.role = TeamMembers.CREATOR
                team_member.save()
        return instance

    class Meta:
        model = Teams
        fields = ['team_title', 'description']


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


class SearchTeamForm(forms.Form):

    search_str = forms.CharField(
        widget=forms.TextInput(attrs={

        }),
        label="Поиск"
    )

    is_open = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={

        }),
        required=False,
        label="Происходит набор"
    )
