from django import forms

from translators_hub.models import UserProfile


class ServiceForm(forms.Form):
    cleaned_data = {}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
