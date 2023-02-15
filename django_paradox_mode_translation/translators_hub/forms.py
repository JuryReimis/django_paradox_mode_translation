from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.db import models

import translators_hub.models
from translators_hub.models import UserProfile, ModTranslation, Invites, Roles

User = get_user_model()


class ServiceForm(forms.Form):
    cleaned_data = {}


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)
        field_classes = {"username": UsernameField}


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['experience', 'titles', 'description']

    def change_initial_value(self, new_initial_value: dict):
        initial_dict = self.initial
        self.initial = initial_dict | new_initial_value


class ProfileFormForApply(UpdateProfileForm):
    cover_letter = forms.CharField(widget=forms.Textarea, label="Сопроводительное письмо")

    class Meta(UpdateProfileForm.Meta):
        pass


class AddPageForm(forms.ModelForm):

    class Meta:
        model = ModTranslation
        fields = ['title', 'mode_name', 'game', 'steam_link', 'paradox_plaza_link', 'original_language',
                  'target_language']


class InviteUserForm(forms.ModelForm):

    role = forms.ChoiceField(
        choices=Roles.ROLES,
        required=False,
    )

    text_invite = forms.CharField(
        max_length=500,
        label='Приглашение',
        required=False
    )

    class Meta:
        model = Invites
        fields = ['role', 'text_invite']
