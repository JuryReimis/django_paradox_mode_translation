from django.urls import path, include

from . import views

app_name = 'translators_hub'
urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('profile/<slug:slug>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<slug:slug>/invites', views.InvitesView.as_view(), name='invites'),
    path('profile/<slug:slug>/my_projects', views.MyProjectsView.as_view(), name='my_projects'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('add-page', views.AddPageView.as_view(), name='add_page'),
    path('mods-translations/<slug:slug>/', views.DetailView.as_view(), name='detail_page'),
    path('mods-translations/<slug:slug>/management/', views.ManagementView.as_view(), name='management'),
    path('mods-translations/<slug:slug>/management/change_role/username=<str:username>', views.ChangeRoleView.as_view(), name='change_role'),
    path('mods-translations/<slug:slug>/apply-for/', views.ApplyForView.as_view(), name='apply_for'),
    path('mods-translations/<slug:slug>/invite_authors/', views.SendInvitesView.as_view(), name='invite_authors')
]
