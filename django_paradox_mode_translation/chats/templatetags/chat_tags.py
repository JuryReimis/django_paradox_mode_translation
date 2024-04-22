from django.template import Library

from chats.forms import PrivateMessageForm

register = Library()


@register.inclusion_tag(takes_context=True, filename='chats/chat.html')
def get_chats(context):
    user = context['user']
    private_chats = user.private_chats.all().prefetch_related('private_messages', 'private_messages__author')
    private_form = PrivateMessageForm()
    context = {
        'user': user,
        'private_chats': private_chats,
        'teams_chats': None,
        'private_form': private_form
    }
    return context
