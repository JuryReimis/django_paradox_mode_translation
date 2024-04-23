from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.views.generic import FormView

from chats.forms import PrivateMessageForm, TeamMessageForm
from chats.models import PrivateChat, TeamChat


class SendMessageView(FormView):
    private_form_class = PrivateMessageForm
    group_form_class = TeamMessageForm

    def post(self, request, slug=None, *args, **kwargs):
        channel_layer = get_channel_layer()
        chat_type = request.POST.get('chat type')
        form = self.get_form(chat_type=chat_type)
        if form.is_valid():
            if chat_type == "private":
                chat = PrivateChat.objects.get(slug=slug)
            elif chat_type == "team":
                chat = TeamChat.objects.get(slug=slug)
            else:
                return
            instance = form.save(author=request.user, chat=chat)
            formatted_datetime = instance.pub_date.strftime("%Y-%m-%d %H:%M:%S")
            async_to_sync(channel_layer.group_send)(slug, {
                'type': 'message.send.chat',
                'body': request.POST.get('body'),
                'author': request.user.username,
                'pub_date': formatted_datetime
            })
            return JsonResponse({'success': 'ok'})
        else:
            return JsonResponse({'success': 'fault'})

    def get_form(self, form_class=None, chat_type=None):
        if chat_type:
            if chat_type == "private":
                form_class = PrivateMessageForm
            elif chat_type == "team":
                form_class = TeamMessageForm
            else:
                return None
        return super(SendMessageView, self).get_form(form_class)
