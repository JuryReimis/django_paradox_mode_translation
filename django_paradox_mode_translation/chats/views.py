from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.views.generic import FormView

from chats.forms import SendMessageForm
from chats.models import Chat


class SendMessageView(FormView):
    form_class = SendMessageForm

    def post(self, request, slug=None, *args, **kwargs):
        channel_layer = get_channel_layer()
        form = self.get_form()
        if form.is_valid():
            chat = Chat.objects.get(slug=slug)
            instance = form.save(author=request.user, chat=chat)
            formatted_datetime = instance.pub_date.strftime("%Y-%m-%d %H:%M:%S")
            async_to_sync(channel_layer.group_send)(slug, {
                'type': 'message.send.chat',
                'body': request.POST.get('body'),
                'author': request.user.username,
                'pub_date': formatted_datetime
            })
        return JsonResponse({})
