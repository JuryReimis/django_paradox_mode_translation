from django.urls import path

from moderators.views import ModeratorHomeView, SendQueryView

app_name = 'moderators'

urlpatterns = [
    path('', ModeratorHomeView.as_view(), name='home'),
    path('send-query/', SendQueryView.as_view(), name='send_query'),
]
