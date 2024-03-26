import requests
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from translators_hub.models import UserProfile, Translation, Invites, Roles, Game, ProfileComments, ProjectComments, \
    Language

User = get_user_model()


class ServiceForm(forms.Form):
    cleaned_data = {}


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)
        field_classes = {"username": UsernameField}


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['experience', 'description', 'profile_image']

    def change_initial_value(self, new_initial_value: dict):
        initial_dict = self.initial
        self.initial = initial_dict | new_initial_value


class AddProfileCommentForm(forms.ModelForm):
    comment_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 60,
        }),
        label="Новый комментарий"
    )

    class Meta:
        model = ProfileComments
        fields = ['comment_text']


class ProfileFormForApply(UpdateProfileForm):
    cover_letter = forms.CharField(widget=forms.Textarea, label="Сопроводительное письмо")

    class Meta(UpdateProfileForm.Meta):
        pass


class AddPageForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={

        }),
        label="Название",
    )

    game = forms.ModelChoiceField(
        widget=forms.Select(attrs={

        }),
        queryset=Game.objects.filter(),
        label="Игра"
    )

    original_language = forms.ModelChoiceField(
        widget=forms.Select(attrs={

        }),
        queryset=Language.objects.filter(),
        label="Язык оригинала"
    )

    target_language = forms.ModelChoiceField(
        widget=forms.Select(attrs={

        }),
        queryset=Language.objects.filter(),
        label="Целевой язык"
    )

    class Meta:
        model = Translation
        fields = ['title', 'game', 'original_language',
                  'target_language']


class AddProjectCommentForm(forms.ModelForm):
    comment_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 60,
        }),
        label="Новый комментарий"
    )

    class Meta:
        model = ProjectComments
        fields = ['comment_text']


class ChangeDescriptionForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={

        }),
        label="Название"
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            "cols": 100,
            "rows": 15
        }),
        required=False,
        label="Описание"
    )

    status = forms.ChoiceField(
        choices=Translation.STATUS,
        widget=forms.Select(
            attrs={

            }
        ),
        label="Статус проекта"
    )

    class Meta:
        model = Translation
        fields = ['title', 'image', 'description', 'status']


class InviteUserForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=Roles.ROLES,
        required=False,
    )

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
        model = Invites
        fields = ['role', 'text_invite']


class ChangeUserRoleForm(forms.ModelForm):
    role = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm'
        },),
        choices=Roles.ROLES,
        label="Роль"
    )

    class Meta:
        model = Roles
        fields = ['role', 'user']
        widgets = {'user': forms.HiddenInput()}
