from django.urls import path

from moderators.views import ModeratorHomeView

app_name = 'moderators'

urlpatterns = [
    path('', ModeratorHomeView.as_view(), name='home'),
]
