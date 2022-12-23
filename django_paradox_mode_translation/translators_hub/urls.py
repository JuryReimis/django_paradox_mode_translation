from django.urls import path

from . import views

app_name = 'translators_hub'
urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('<slug:slug>/', views.DetailView.as_view(), name='detail_page'),
    path('<slug:slug>/apply-for', views.apply_for, name='apply_for')
]
