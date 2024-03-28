from django.urls import path

from moderators.views import ModeratorHomeView, SendQueryView, MyQueriesView

app_name = 'moderators'

urlpatterns = [
    path('', ModeratorHomeView.as_view(), name='home'),
    path('send-query/', SendQueryView.as_view(), name='send_query'),
    path('my-queries/', MyQueriesView.as_view(), name='my_queries'),
]
