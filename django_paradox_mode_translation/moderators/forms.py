from django import forms

from moderators.models import Query, Topic
from translators_hub.models import Game


class SendQueryForm(forms.ModelForm):

    query_text = forms.CharField(
        widget=forms.Textarea(attrs={

        }),
        required=True,
        label="Текст заявки"
    )

    topic = forms.ModelChoiceField(
        widget=forms.Select(attrs={

        }),
        queryset=Topic.objects.filter(),
        label="Тема заявки"
    )

    class Meta:
        model = Query
        fields = ['query_text', 'topic']


class QueryDenialForm(forms.ModelForm):

    denial_reason = forms.CharField(
        widget=forms.Textarea(attrs={

        }),
        required=True,
        label="Основания для отказа"
    )

    class Meta:
        model = Query
        fields = ['denial_reason']


class AddGameForm(forms.ModelForm):

    game_name = forms.CharField(
        widget=forms.TextInput(attrs={

        }),
        required=True,
        label="Название игры"
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={

        }),
        required=False,
        label="Описание"
    )

    class Meta:
        model = Game
        fields = ['game_name', 'description']
