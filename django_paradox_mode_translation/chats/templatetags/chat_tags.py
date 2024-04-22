from django.template import Library

from chats.forms import PrivateMessageForm
from chats.models import TeamChat

register = Library()


@register.inclusion_tag(takes_context=True, filename='chats/chat.html')
def get_chats(context):
    user = context['user']
    private_chats = user.private_chats.all().prefetch_related('private_messages', 'private_messages__author')
    private_form = PrivateMessageForm()
    team_chats = []
    for team_member in user.membership.all().select_related('team', 'team__team_chat'):
        try:
            chat = team_member.team.team_chat
        except AttributeError as error:
            print(f"Не обнаружен чат команды {team_member.team.team_title}", error, "Создаю новую запись...")
            chat = TeamChat.objects.create(team=team_member.team,
                                           **TeamChat.get_chat_params(team_member.team.team_title))
        team_chats.append(chat)

    context = {
        'user': user,
        'private_chats': private_chats,
        'teams_chats': team_chats if team_chats else None,
        'private_form': private_form
    }
    return context
