import requests
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField


from translators_hub.models import UserProfile, ModTranslation, Invites, Roles, Game, Titles, AbstractComments, \
    ProfileComments

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

    mode_name = forms.CharField(
        widget=forms.TextInput(attrs={

        }),
        label="Название оригинального мода"
    )

    game = forms.ModelChoiceField(
        widget=forms.Select(attrs={

        }),
        queryset=Game.objects.filter(),
        label="Игра"
    )

    steam_link = forms.URLField(
        widget=forms.URLInput(attrs={

        }),
        empty_value=None,
        required=False,
        label="Ссылка на страницу мода в Steam"
    )

    paradox_plaza_link = forms.URLField(
        widget=forms.URLInput(attrs={

        }),
        empty_value=None,
        required=False,
        label="Ссылка на страницу мода на ParadoxPlaza"
    )

    original_language = forms.ChoiceField(
        widget=forms.Select(attrs={

        }),
        choices=ModTranslation.VALID_LANGUAGES,
        initial=ModTranslation.ENGLISH,
        label="Язык оригинала"
    )

    target_language = forms.ChoiceField(
        widget=forms.Select(attrs={

        }),
        choices=ModTranslation.VALID_LANGUAGES,
        initial=ModTranslation.RUSSIAN,
        label="Целевой язык"
    )

    class Meta:
        model = ModTranslation
        fields = ['title', 'mode_name', 'game', 'steam_link', 'paradox_plaza_link', 'original_language',
                  'target_language']


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

    steam_link = forms.URLField(
        widget=forms.URLInput(attrs={
            "size": 100
        }),
        required=False,
        label="Ссылка на оригинал мода в Steam"
    )

    paradox_plaza_link = forms.URLField(
        widget=forms.URLInput(attrs={
            "size": 100
        }),
        required=False,
        label="Ссылка на оригинал мода на Paradox Plaza"
    )

    status = forms.ChoiceField(
        choices=ModTranslation.STATUS,
        widget=forms.Select(
            attrs={

            }
        ),
        label="Статус проекта"
    )

    def clean_steam_link(self):
        steam_link = self.cleaned_data['steam_link']
        if steam_link:
            response = requests.get(steam_link)
            if response.status_code != 200:
                raise forms.ValidationError("Страницы с таким адресом не существует")
        return steam_link

    def clean_paradox_plaza_link(self):
        paradox_plaza_link = self.cleaned_data['paradox_plaza_link']
        if paradox_plaza_link:
            response = requests.get(paradox_plaza_link)
            if response.status_code != 200:
                raise forms.ValidationError("Страницы с таким адресом не существует")
        return paradox_plaza_link

    class Meta:
        model = ModTranslation
        fields = ['title', 'image', 'description', 'steam_link', 'paradox_plaza_link', 'status']


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
