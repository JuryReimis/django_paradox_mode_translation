from django.urls import path

from teams import views

app_name = 'teams'

urlpatterns = [
    path('', views.TeamsView.as_view(), name='home'),
    path('create_team/', views.CreateTeamView.as_view(), name='create_team'),
    path('invites/', views.TeamInvitesHandler.as_view(), name='invites'),
    path('<slug:slug>/', views.TeamPageView.as_view(), name='team_detail'),
    path('<slug:slug>/invite_users/', views.SendInviteView.as_view(), name='invite_user'),
]
