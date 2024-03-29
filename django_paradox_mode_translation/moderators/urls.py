from django.urls import path

from moderators.views import ModeratorHomeView, SendQueryView, MyQueriesView, QueryBookingView, QueriesInWorkView

app_name = 'moderators'

urlpatterns = [
    path('', ModeratorHomeView.as_view(), name='home'),
    path('send-query/', SendQueryView.as_view(), name='send_query'),
    path('my-queries/', MyQueriesView.as_view(), name='my_queries'),
    path('query-booking/', QueryBookingView.as_view(), name='query_booking'),
    path('queries-in-work/', QueriesInWorkView.as_view(), name='queries_in_work')
]
