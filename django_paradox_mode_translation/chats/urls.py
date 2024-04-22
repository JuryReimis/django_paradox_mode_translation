from django.urls import path

from chats.views import SendMessageView

app_name = 'chats'

urlpatterns = [
    path('<slug:slug>/', SendMessageView.as_view(), name='send_message')
]
