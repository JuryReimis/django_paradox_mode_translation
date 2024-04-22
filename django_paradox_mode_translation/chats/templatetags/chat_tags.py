from django.template import Library

from chats.forms import SendMessageForm

register = Library()


@register.inclusion_tag(takes_context=True, filename='chats/chat.html')
def get_chats(context):
    user = context['user']
    user_chats = user.chats.all().prefetch_related('messages', 'messages__author')
    form = SendMessageForm()
    context = {
        'user': user,
        'user_chats': user_chats,
        'form': form
    }
    return context
